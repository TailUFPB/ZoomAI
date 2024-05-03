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

if __name__ == '__main__':
    PORT = 8000
    http_tunnel = ngrok.connect(PORT)
    public_url = http_tunnel.public_url
    HOST_URL = public_url

    print(f"Public URL: {public_url}")
    uvicorn.run("api:app", host="127.0.0.1", port=PORT, log_level="info", workers=1)

