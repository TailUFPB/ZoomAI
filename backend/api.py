from fastapi import FastAPI, Query
import sys
import os
import asyncio
from datetime import datetime

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
sys.path.append(os.path.join(parent_dir, 'models'))

from status_return import *
from models.generate_images import Generator

#adding cors headers
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI()
g = Generator()

task = None

database = g.get_database()

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
async def create_infinite_zoom(prompt: str = Query(None)):
    global task
    try:
        prompt_gpt = await g.gpt_prompt_create(prompt)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        project_id = database.insert_project(prompt, None, now, prompt_gpt)
        task = asyncio.create_task(g.sd_generate_image(prompt_gpt,project_id))

        return {"status": 200}
    except Exception as e:  
        print(e)
        return {"status": 500}


@app.get('/check')
async def check_status():
    global task
    if task:
        return {"status": RUNNING if not task.done() else DONE}
    else:
        return {"status": NO_TASK}
    

@app.post('/stop')
async def stop():
    global task
    if task:
        task.cancel()
        task = None
        return {"status": 200}
    else:
        return {"status": NO_TASK}

@app.get('/save')
async def save_image():
    global task
    if task and task.done():
        g.read_image_from_db(10)
        return {"status": 200}
    else:
        return {"status": NO_TASK}




