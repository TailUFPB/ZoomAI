from db_utils import Database
import PIL
from PIL import Image
from io import BytesIO
import zipfile

db = Database()

result = db.get_all_projects()

for project_id, project in result.items():
    if project['images']:
        images = project['images']
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
            for i, image in enumerate(images):
                image = Image.open(BytesIO(image))
                image.save(f'{i}.png')
                zip_file.write(f'{i}.png')

        project['images'] = zip_buffer.getvalue()
        print(project)
        zip_buffer.close()
    else:
        project['images'] = None
