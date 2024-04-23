from diffusers import StableDiffusionInpaintPipeline, EulerAncestralDiscreteScheduler
from database.db_utils import Database
from openai import OpenAI
from PIL import Image
from datetime import datetime
import threading
import numpy as np
import torch
import os
import io

class Generator:
    def __init__(self):
        self.actual_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db = Database()
        self.inpaint_model_list = ["stabilityai/stable-diffusion-2-inpainting"]
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"
        self.openai_key = os.environ["OPENAI_API_KEY"] 
        
        self.negative_prompt = "frames, borderline, text, charachter, duplicate, error, out of frame, watermark, low quality, ugly, deformed, blur"
        self.default_prompt = [[0, 'A psychedelic jungle with trees that have glowing, fractal-like patterns, Simon stalenhag poster 1920s style, street level view, hyper futuristic, 8k resolution, hyper realistic']]
        self.num_outpainting_steps = 40
        self.guidance_scale = 7
        self.num_inference_steps = 50
        self.custom_init_image = None
        self.project_id = None

        self.all_frames = []
        self.mutex = threading.Lock()
        self.sem = threading.Semaphore(0)
        self.image_order = 0
        self.end_thread = False

        self.pipe = StableDiffusionInpaintPipeline.from_pretrained(
            self.inpaint_model_list[0],
            torch_dtype=torch.float16,
        )

        self.pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(
            self.pipe.scheduler.config)
        self.pipe = self.pipe.to("cuda")

        self.pipe.safety_checker = None
        self.pipe.enable_attention_slicing()
        
        self.skip_frames = 10
    
    def read_image_from_db(self, project_id):
        images = self.db.get_images(project_id)
        count = 0

        for image in images:
            image = image[0]
            image = Image.open(io.BytesIO(image))
            
            image_path = f"images/{project_id}"
            if not os.path.exists(image_path):
                os.makedirs(image_path)
            image.save(f"{image_path}/{count}.png")
            count += 1 

    def save_image_in_db(self):
        thread_db = Database()
        while True:
            self.sem.acquire()
            self.mutex.acquire()
            if len(self.all_frames) > 0:
                if self.image_order % self.skip_frames == 0:
                    frame = self.all_frames.pop(0)
                    imgByteArr = io.BytesIO()
                    frame.save(imgByteArr, format="PNG")
                    imgByteArr = imgByteArr.getvalue()

                    self.mutex.release()

                    thread_db.insert_image(self.project_id, imgByteArr, int((self.image_order)//self.skip_frames))
                    print(f"frame {int((self.image_order)//self.skip_frames)} saved")
                else:
                    self.mutex.release()
                    self.all_frames.pop(0)
                self.image_order += 1
            else:
                self.mutex.release()
                if self.end_thread: break

    def findAvailableFilename(self, base_name):
        # Check if the path with the name is already exist
        index = 1
        while True:
            file_name = f"{base_name}{index}.json"
            if not os.path.exists(file_name):
                return file_name
            index += 1

    def sanity_check_string(self, input_string):
        # Remove spaces and convert to lowercase
        sanitized_string = input_string.replace(" ", "").lower()
        return sanitized_string

    def saveResponse(self, response, userInput):
        # Save the response
        userInputsanity = self.sanity_check_string(userInput)
        #  but only the message
        messageContent = response.choices[0].message.content
        fileName = self.findAvailableFilename(userInputsanity)
        with open(fileName, 'w') as file:
            file.write(messageContent)

    def gpt_prompt_create(self, userInput):
        client = OpenAI(api_key= self.openai_key)

        with open('jsonSchema.txt', 'r') as f:
            jsonSchema = f.read()

        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "using the JSON attached, keeping the same struct and change everything to the theme of user input."},
                {"role": "assistant", "content": "create 10 new elements on data. By starting with 0, increase the number by 5 each time"},
                {"role": "user", "content": userInput},
                {"role": "assistant", "content": jsonSchema},     
            ] 
                
        )   
        return response

    def sd_generate_image(
        self, 
        prompts_array, project_id
    ):
        
        if not prompts_array: 
            prompts_array = self.default_prompt

        self.project_id = project_id
        self.end_thread = False

        prompts = {}
        for x in prompts_array:
            try:
                key = int(x[0])
                value = str(x[1])
                prompts[key] = value
            except ValueError:
                pass

        g_cuda = torch.Generator(device='cuda')

        height = 800
        width = height

        current_image = Image.new(mode="RGBA", size=(height, width))
        mask_image = np.array(current_image)[:, :, 3]
        mask_image = Image.fromarray(255-mask_image).convert("RGB")
        current_image = current_image.convert("RGB")
        
        if (self.custom_init_image):
            current_image = self.custom_init_image.resize(
                (width, height), resample=Image.LANCZOS)
        else:
            init_images = self.pipe(prompt=prompts[min(k for k in prompts.keys() if k >= 0)],
                            negative_prompt=self.negative_prompt,
                            image=current_image,
                            guidance_scale=self.guidance_scale,
                            height=height,
                            width=width,
                            mask_image=mask_image,
                            num_inference_steps=self.num_inference_steps)[0]
            current_image = init_images[0]
        mask_width = 128
        num_interpol_frames = 30

        #start consumer thread
        consumer_thread = threading.Thread(target=self.save_image_in_db)
        consumer_thread.start()
        
        self.all_frames.append(current_image)
        self.sem.release()

        for i in range(self.num_outpainting_steps):
            print('Outpaint step: ' + str(i+1) +
                ' / ' + str(self.num_outpainting_steps))

            prev_image_fix = current_image

            prev_image = self.shrink_and_paste_on_blank(current_image, mask_width)

            current_image = prev_image

            # create mask (black image with white mask_width width edges)
            mask_image = np.array(current_image)[:, :, 3]
            mask_image = Image.fromarray(255-mask_image).convert("RGB")

            # inpainting step
            current_image = current_image.convert("RGB")
            images = self.pipe(prompt=prompts[max(k for k in prompts.keys() if k <= i)],
                        negative_prompt=self.negative_prompt,
                        image=current_image,
                        guidance_scale=self.guidance_scale,
                        height=height,
                        width=width,
                        # generator = g_cuda.manual_seed(seed),
                        mask_image=mask_image,
                        num_inference_steps=self.num_inference_steps)[0]
            current_image = images[0]
            current_image.paste(prev_image, mask=prev_image)

            # interpolation steps bewteen 2 inpainted images (=sequential zoom and crop)
            for j in range(num_interpol_frames - 1):
                interpol_image = current_image
                interpol_width = round(
                    (1 - (1-2*mask_width/height)**(1-(j+1)/num_interpol_frames))*height/2
                )
                interpol_image = interpol_image.crop((interpol_width,
                                                    interpol_width,
                                                    width - interpol_width,
                                                    height - interpol_width))

                interpol_image = interpol_image.resize((height, width))

                # paste the higher resolution previous image in the middle to avoid drop in quality caused by zooming
                interpol_width2 = round(
                    (1 - (height-2*mask_width) / (height-2*interpol_width)) / 2*height
                )
                prev_image_fix_crop = self.shrink_and_paste_on_blank(
                    prev_image_fix, interpol_width2)
                interpol_image.paste(prev_image_fix_crop, mask=prev_image_fix_crop)

                self.all_frames.append(interpol_image)
                self.sem.release()

            self.all_frames.append(current_image)
            self.sem.release()

            self.end_thread = True
        
        return 200

    def shrink_and_paste_on_blank(self, current_image, mask_width):

        height = current_image.height
        width = current_image.width

        #shrink down by mask_width
        prev_image = current_image.resize((height-2*mask_width,width-2*mask_width))
        prev_image = prev_image.convert("RGBA")
        prev_image = np.array(prev_image)

        #create blank non-transparent image
        blank_image = np.array(current_image.convert("RGBA"))*0
        blank_image[:,:,3] = 1

        #paste shrinked onto blank
        blank_image[mask_width:height-mask_width,mask_width:width-mask_width,:] = prev_image
        prev_image = Image.fromarray(blank_image)

        return prev_image

    def get_database(self):
        return self.db
