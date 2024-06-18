from fastapi import FastAPI, Query,BackgroundTasks,HTTPException
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from time import sleep

class TestClass:
    def __init__(self) -> None:
        self.file_status_path = "status"

    def generate_images(self,prompt): 
        self.start_running()
        
        for i in range(50):
            print(f"[{i}] running... {prompt}")
            sleep(1)
        print("done")

        self.stop_running()
        

    def start_running(self):
        with open(self.file_status_path, 'w') as f:
            f.write("1")
    def stop_running(self):
        with open(self.file_status_path, 'w') as f:
            f.write("0")
    def get_status(self):
        with open(self.file_status_path, 'r') as f:
            return f.read() == "1"

app = FastAPI()

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

test = TestClass()

@app.get('/create/{prompt}')
async def test_async(prompt: str , background_tasks: BackgroundTasks ):
    print("checking status: ",test.get_status())
    if test.get_status():
        return 400
    
    print("started generating images")

    background_tasks.add_task(test.generate_images,prompt)
    return 200

