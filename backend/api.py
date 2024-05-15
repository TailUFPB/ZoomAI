from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import StreamingResponse
import sys
import os
from datetime import datetime
from io import BytesIO
import zipfile


parent_dir = os.path.abspath(os.path.join(os.path.dirname(_file_), os.pardir))
sys.path.append(parent_dir)
sys.path.append(os.path.join(parent_dir, 'models'))

from status_return import *
from models.generate_images import Generator

#adding cors headers
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI()
g = Generator()

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

# Rota para buscar todas as imagens de um projeto com o parâmetro id_do_projeto
@app.get('/get_images/{id_project}')
async def get_images(id_project: int):

    # Busca objetos de imagem diretamente do banco de dados
    images = database.get_images_from_project(id_project)
    if not images:
        raise HTTPException(status_code=404, detail="No images found for this project")

    # Object BytesIO -> ZIP em memória
    memory_zip = BytesIO()

    # Cria um novo arquivo ZIP no objeto BytesIO
    with zipfile.ZipFile(memory_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for image_record in images:
            # imagens estão em bytes.
            img = Image.open(BytesIO(image_record.image_data))
            
            # Converte para PNG e salva em um BytesIO temporário
            img_bytes = BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            # Adiciona ao ZIP
            zf.writestr(f"{image_record.image_name}.png", img_bytes.getvalue())

    # Apontar o ponteiro para o início do arquivo para leitura
    memory_zip.seek(0)

    # Retorna o arquivo ZIP como uma resposta de streaming
    return StreamingResponse(memory_zip, media_type="application/zip")