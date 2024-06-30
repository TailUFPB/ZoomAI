<h1>ZoomAI</h1>

### Overview

This project allows users to generate "infinite zoom" art based on their textual and visual inputs. Leveraging advanced models such as ChatGPT for prompt generation and Stable Diffusion for image inpainting and generation, the application takes user inputs to create detailed prompts and produces seamless, infinitely zoomable images. Users can explore and zoom into the created artworks. The primary aim is to offer a unique and immersive experience through captivating "infinite zoom" art.

### Image Generation and Manipulation Pipeline

![Imagem do WhatsApp de 2024-06-17 à(s) 22 26 10_03e5fdfe](https://github.com/TailUFPB/ZoomAI/assets/100447684/00cece69-ba1a-46ec-86ee-51dfb9eb84cf)

1. User Input: The pipeline accepts two types of inputs from users:
* Text Input: User-provided text describing the desired image.
* Image Input: User-provided image to be used as a reference.

2. Image to Text Model: Uses Salesforce's blip-image-captioning-large model to convert image inputs into text descriptions.

3. ChatGPT API: Utilizes OpenAI's gpt-3.5-turbo-0125 to process user prompts and generate detailed prompts for the image generation model.

4. Database: Stores project information and image data, including user prompts, generated prompts, and images.

5. Stable Diffusion Model: Uses StabilityAI's stable-diffusion-2-inpainting for generating and inpainting images based on the processed prompts.

6. Producer and Consumer:
* Producer: Handles the image generation process.
* Consumer: Manipulates and processes the generated images.

### Setup

```sh
git clone https://github.com/TailUFPB/ZoomAI
cd ZoomAI
```

```py
pip install -r requirements.txt
```

### Running Instructions

#### **Important Notes**
* GPU Requirement: This project requires a GPU to run.
* Environment Configuration: You need to update the environment configuration in `common/environment.js` in the frontend to point to where the backend will be running.

#### Backend
1. In the project's root directory, run:

```py
pyton3 backend/api.py
```

#### Frontend
1. Navigate to the frontend directory and install frontend dependencies:
```sh
cd frontend
npm start
```

2. Start the frontend:
```sh
npm start
```

