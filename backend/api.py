from fastapi import FastAPI, Query
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
sys.path.append(os.path.join(parent_dir, 'models'))

from models.generate_images import Generator

#adding cors headers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
g = Generator()

# adding cors urls
origins = [
    'http://localhost:3000'
]

# add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins= origins, 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"]
)

default_params = {
    "model_id": g.inpaint_model_list[0],
    "prompts_array": g.default_prompt,
    "negative_prompt": g.default_negative_prompt,
    "num_outpainting_steps": g.num_outpainting_steps,
    "guidance_scale": g.guidance_scale,
    "num_inference_steps": g.num_inference_steps,
    "custom_init_image": None
}

@app.get('/create')
async def create_infinite_zoom(model_id: str = Query(default=default_params["model_id"]), 
                               prompts_array: str = Query(default=default_params["prompts_array"]), 
                               negative_prompt: str = Query(default=default_params["negative_prompt"]), 
                               num_outpainting_steps: int = Query(default=default_params["num_outpainting_steps"]), 
                               guidance_scale: float = Query(default=default_params["guidance_scale"]), 
                               num_inference_steps: int = Query(default=default_params["num_inference_steps"]), 
                               custom_init_image: str = Query(default=default_params["custom_init_image"])):
    
    # gpt_prompt = await g.gpt_prompt_create(prompt)

    print("Query Params: ", model_id, prompts_array, negative_prompt, num_outpainting_steps, guidance_scale, num_inference_steps, custom_init_image)
    img_response = await g.sd_generate_image(model_id, prompts_array, negative_prompt, num_outpainting_steps, guidance_scale, num_inference_steps, custom_init_image)
    return {"status" : "ok", "data" : img_response}




