from fastapi import FastAPI, Query
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from time import sleep

app = FastAPI()

task = None

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

async def generate_images():
    for i in range(20):
        print(f"[{i}] running...")
        sleep(1)
    print("done")


@app.get('/create')
async def test_async(prompt: str = Query(None)):
    global task
    print("started generating images")
    task = asyncio.create_task(generate_images())
    return {"message": "Images are being generated"}

@app.get('/check')
async def check_status():
    global task
    if task:
        return {"status": "running" if not task.done() else "finished"}
    else:
        return {"status": "no task started"}

