from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse
import sys
import os
from datetime import datetime
from io import BytesIO
import zipfile
import base64
from typing import List
from io import BytesIO
import zipfile
import base64
from typing import List

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
sys.path.append(os.path.join(parent_dir, 'models'))

from status_return import *
from models.generate_images import Generator

#adding cors headers
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pyngrok import ngrok
import uvicorn

app = FastAPI()
g = Generator()

database = g.get_database()

# adding cors urls
origins = [
    'http://localhost:3000',
    'http://localhost:8000',
    'http://localhost:5000',
]

# add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins= origins, 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"]
)

#! see what database is returning
@app.get('/get_images/{id}')
async def get_images(id: int):
    images = database.get_images(id)

    if not images:
        return HTTPException(status_code=404, detail="Project not found")

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        for i, image in enumerate(images):
            zip_file.writestr(f'{i}.png', image[0])
    
    response = StreamingResponse(iter([zip_buffer.getvalue()]), media_type='application/zip')
    response.headers['Content-Disposition'] = f'attachment; filename=images.zip'

    return response 

@app.get('/get_projects')
async def get_projects():
    projects = database.get_all_projects()

    for project_id, project in projects.items():
        images = project['images']
        if images:
            base64_images = [base64.b64encode(image).decode('utf-8') for image in images]
            project['images'] = base64_images

    return projects



@app.get('/create/{prompt}')
async def create_infinite_zoom(prompt: str, background_tasks: BackgroundTasks):
    
    if g.is_running():
        return RUNNING
    
    try:
        prompt_gpt = await g.gpt_prompt_create(prompt)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        project_id = database.insert_project(prompt, None, now, prompt_gpt)
        background_tasks.add_task(g.generate_images, prompt_gpt, project_id)

        return STARTED
    
    except Exception as e:  
        print(e)
        return ERROR

#! using this rout to save the images in a path on aria2
@app.get('/savepath/{project_id}')
async def save_image(project_id: int):
    if not g.is_running():
        g.read_image_from_db(project_id)
        return 200
    else:
        return 400



if __name__ == '__main__':
    PORT = 8000
    http_tunnel = ngrok.connect(PORT)
    public_url = http_tunnel.public_url
    HOST_URL = public_url

    print(f"Public URL: {public_url}")
    uvicorn.run("api:app", host="127.0.0.1", port=PORT, log_level="info", workers=1)

