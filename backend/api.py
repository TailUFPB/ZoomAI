from fastapi import FastAPI, Query
import sys
import os
import asyncio
from datetime import datetime

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
sys.path.append(os.path.join(parent_dir, 'models'))


from models.generate_images import Generator

#adding cors headers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
g = Generator()

database = g.db

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
    prompt_gpt = await g.gpt_prompt_create(prompt)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    project_id = database.insert_project(prompt, "see what to put here", now, prompt_gpt)

    status = g.sd_generate_image(prompt_gpt, project_id)

    print("started generating images")

    return {"status" : "running", "code" : status}




