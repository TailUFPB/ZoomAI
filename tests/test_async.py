from fastapi import FastAPI, Query,BackgroundTasks,HTTPException
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from time import sleep

app = FastAPI()

task = False

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

def generate_images():
    global task
    for i in range(20):
        print(f"[{i}] running...")
        sleep(1)
    print("done")
    task = False



@app.get('/create/{prompt}')
async def test_async(prompt: str , background_tasks: BackgroundTasks ):
    print("prompt: ", prompt)
    global task
    if task:
        return 400
    print("started generating images")
    task = True
    background_tasks.add_task(generate_images)
    return 200

