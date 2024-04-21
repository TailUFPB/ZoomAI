from fastapi import FastAPI, Query
import sys
import os
import asyncio

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
    
    # gpt_prompt = await g.gpt_prompt_create(prompt)
    # img_response = await g.sd_generate_image(prompts_array=[(0, prompt)])
    asyncio.create_task(g.sd_generate_image(prompts_array=[(0, prompt)]))

    print("started generating images")

    return {"status" : "running"}




