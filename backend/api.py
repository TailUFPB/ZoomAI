from fastapi import FastAPI, BackgroundTasks, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import sys
import os
import re
from datetime import datetime
from io import BytesIO
import zipfile
import base64
from typing import List
from PIL import Image

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
sys.path.append(os.path.join(parent_dir, 'models'))

from status_return import *
from letters import vowels, consonants
from models.generate_images import Generator


#adding cors headers
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn

app = FastAPI()

static_path = os.path.join(os.path.dirname(__file__), 'static')
app.mount("/static", StaticFiles(directory=static_path), name="static")

g = Generator()

database = g.get_database()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

# add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"]
)

@app.get("/")
async def read_root():
    return {"message": "hello world, api zoomai"}


@app.get('/get_projects')
async def get_projects():
    projects = database.get_all_projects()

    for project_id, project in projects.items():
        cover = project['cover']
        if cover:
            base64_cover = base64.b64encode(cover).decode('utf-8')
            projects[project_id]['cover'] = base64_cover

    return projects

@app.get('/get_images/{id}')
async def get_images(id: int):
    images = database.get_images(id)

    if images:
        try:
            for index, image in enumerate(images):
                base64_images = [base64.b64encode(image).decode('utf-8') for image in images]
            return {"images": base64_images}
        
        except Exception as e:
            print("Error: ", e)
            return ERROR

def verifyWord(word):
    if len(word) > 2:
        if re.search(vowels, word, re.IGNORECASE) and re.search(consonants, word, re.IGNORECASE):
            return True
    elif len(word) == 2:
        if re.search(vowels, word, re.IGNORECASE):
            return True
    return False

@app.post('/create_fake/{prompt}')
async def create_fake_route(prompt: str, background_tasks: BackgroundTasks):
    if g.is_running():
        return RUNNING
    
    for index, word in enumerate(prompt.split()):
        if (len(word) <= 30):
            if (verifyWord(word) or word.isnumeric()):
                continue
            else:
                return INVALID
        else:
            return INVALID
    
    return STARTED

@app.post('/upload')
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if g.is_running():
        return RUNNING

    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        file_content = await file.read()
        start_prompt = await g.get_image_description(BytesIO(file_content))

        print("Start Prompt : ", start_prompt)

        prompt_gpt = await g.gpt_prompt_create(start_prompt)
        prompt_text = prompt_gpt[0][1]

        project_id = database.insert_project(start_prompt, now, prompt_text)


        background_tasks.add_task(g.sd_generate_image, prompt_gpt, project_id, file_content)
        return STARTED
    
    except Exception as e:
        print("Error: ", e)
        return ERROR


@app.post('/create/{prompt}')
async def create_infinite_zoom(prompt: str, 
                               background_tasks: BackgroundTasks):  
    
    if g.is_running():
        return RUNNING
    
    print("Is running: ", g.is_running())
    for index, word in enumerate(prompt.split()):
        if (len(word) <= 30):
            if (verifyWord(word) or word.isnumeric()):
                continue
            else:
                return INVALID
        else:
            return INVALID
    
    try:
        prompt_gpt = await g.gpt_prompt_create(prompt)
        prompt_text = prompt_gpt[0][1]
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        project_id = database.insert_project(prompt, now, prompt_text)
        
        background_tasks.add_task(g.sd_generate_image, prompt_gpt, project_id)

        return STARTED
    
    except Exception as e:  
        print("Error: ", e)
        return ERROR

if __name__ == '__main__':
    HOST = "0.0.0.0"  # Use 0.0.0.0 to bind to all available interfaces
    PORT = 8000 # Replace with your desired port number

    uvicorn.run("api:app", host=HOST, port=PORT, log_level="info", workers=1, reload=True)
