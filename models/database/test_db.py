from db_utils import Database
import PIL
from PIL import Image
from io import BytesIO
import zipfile

db = Database()
db.delete_project(24)