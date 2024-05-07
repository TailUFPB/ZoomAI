from fastapi import FastAPI
import sys
import os
import base64

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
sys.path.append(os.path.join(parent_dir, 'models'))

from models.database.db_utils import Database
from models.generate_images import Generator

#adding cors headers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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

@app.get('/create')
async def create_infinite_zoom(prompt, model_id, negative_prompt, 
        num_outpainting_steps, guidance_scale, num_inference_steps,
        custom_init_image):
    g = await Generator()
    better_prompt = await g.gpt_prompt_create(prompt)
    imgs = await g.sd_generate_image(model_id, better_prompt, negative_prompt, num_outpainting_steps,
                guidance_scale, num_inference_steps,custom_init_image)
    return {"status" : "ok", "data" : imgs}

async def convert_imgs_to_base64(projects):
    for project_id, project in projects.items():
        images = project.get("images", [])
        decoded_images = []
        for image in images:
            decoded_image = base64.b64decode(image)
            decoded_images.append(decoded_image)
        project["images"] = decoded_images
    return projects

@app.get('/projects')
async def visualize_all_projects():
    db = await Database()
    projects = await db.get_all_projects()
    if not projects:
        return
    projects_with_imgs_decoded = convert_imgs_to_base64(projects)
    return projects_with_imgs_decoded

@app.get('/project/{project_id}')
async def visualize_project(project_id: int):
    db = await Database()
    project = await db.get_images(project_id)
    if not project:
        return
    project_with_img_decoded = convert_imgs_to_base64(project)
    return project_with_img_decoded
