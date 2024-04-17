import os
from database.db_utils import Database
import base64 # need for encoding generated images
from datetime import datetime

class Generator:
    def __init__(self):
        self.actual_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db = Database()
        print(type(self.actual_date))

    def gpt_prompt_create(self, prompt):
        pass

    def sd_generate_image(self, prompt):
        pass

g=Generator()