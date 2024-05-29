from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse
import sys
import os
import re
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
from letters import vowels, consonants
from models.generate_images import Generator


#adding cors headers
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pyngrok import ngrok
import uvicorn

app = FastAPI()
g = Generator()

database = g.get_database()

# add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"]
)

@app.get('/get_projects')
async def get_projects():
    projects = database.get_all_projects()

    for project_id, project in projects.items():
        images = project['images']
        if images:
            base64_images = [base64.b64encode(image).decode('utf-8') for image in images]
            project['images'] = base64_images

    return projects

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
        

@app.post('/create/{prompt}')
async def create_infinite_zoom(prompt: str, background_tasks: BackgroundTasks):
    
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
    PORT = 8000
    http_tunnel = ngrok.connect(PORT)
    public_url = http_tunnel.public_url
    HOST_URL = public_url

    print(f"Public URL: {public_url}")
    uvicorn.run("api:app", host="127.0.0.1", port=PORT, log_level="info", workers=1, reload=True)

