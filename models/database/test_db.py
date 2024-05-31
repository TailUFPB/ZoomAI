from db_utils import Database
import PIL
from PIL import Image
from io import BytesIO
import zipfile

db = Database()

result = db.get_all_projects()