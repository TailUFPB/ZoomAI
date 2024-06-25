<h1>ZoomAI</h1>

## Image Generation and Manipulation Pipeline

![Imagem do WhatsApp de 2024-06-17 à(s) 22 26 10_03e5fdfe](https://github.com/TailUFPB/ZoomAI/assets/100447684/00cece69-ba1a-46ec-86ee-51dfb9eb84cf)

### Overview

This project allows users to generate and manipulate images based on textual and visual inputs. The pipeline leverages models such as ChatGPT for prompt generation and Stable Diffusion for image inpainting and generation. The core steps involve taking user inputs, generating prompts, and producing final images.

### Components
1. User Input: The pipeline accepts two types of inputs from users:
* Text Input: User-provided text describing the desired image.
* Image Input: User-provided image to be used as a reference.

2. Image to Text Model: Uses Salesforce's blip-image-captioning-large model to convert image inputs into text descriptions.

3. ChatGPT API: Utilizes OpenAI's gpt-3.5-turbo-0125 to process user prompts and generate detailed prompts for the image generation model.

4. Database: Stores project information and image data, including user prompts, generated prompts, and images.

5. Stable Diffusion Model: Uses StabilityAI's stable-diffusion-2-inpainting for generating and inpainting images based on the processed prompts.

6. Producer and Consumer:
* Producer: Handles the image generation and manipulation process.
* Consumer: Delivers the final images to the user.

### Setup

```sh
git clone https://github.com/TailUFPB/ZoomAI
cd ZoomAI
```

```py
pip install -r requirements.txt
```

