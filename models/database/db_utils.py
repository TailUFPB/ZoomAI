import sqlite3
import os

class Database:
    database_file = os.path.join(os.path.dirname(__file__), 'zoomai_database.db')
    def __init__(self, dpath = database_file):

        if not os.path.exists(dpath):
            os.mknod(dpath)

        self.conn = sqlite3.connect(dpath)
        self.cursor = self.conn.cursor()

        self.create_db() if not self.tables_exist() else None

    def create_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, cover BLOB, created_at TEXT, prompts TEXT)
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, image BLOB,  image_order INTEGER ,FOREIGN KEY(project_id) REFERENCES projects(id))
        ''')
    
        self.conn.commit()

        print('database created')

    def insert_project(self, name, cover, created_at, prompts):
        self.cursor.execute('''
            INSERT INTO projects (name, cover, created_at, prompts) VALUES (?, ?, ?, ?)
        ''', (name, cover, created_at, prompts))

        self.conn.commit()

        return self.cursor.lastrowid

        

    def insert_image(self, project_id, image, image_order):
        self.cursor.execute('''
            INSERT INTO images (project_id, image, image_order) VALUES (?, ?, ?)
        ''', (project_id, image, image_order))

        self.conn.commit()

    def get_all_projects(self):
        self.cursor.execute('''
            SELECT * FROM projects
        ''')

        projects = self.cursor.fetchall()

        return projects

    def get_images(self, project_id):
        self.cursor.execute('''
            SELECT image FROM images WHERE project_id = ? ORDER BY image_order DESC
        ''', (project_id,))

        images = self.cursor.fetchall()

        return images
    
    def tables_exist(self):
        self.cursor.execute('''
            SELECT name FROM sqlite_master WHERE type='table' AND name='projects'
        ''')

        projects = self.cursor.fetchall()

        self.cursor.execute('''
            SELECT name FROM sqlite_master WHERE type='table' AND name='images'
        ''')

        images = self.cursor.fetchall()

        return len(projects) > 0 and len(images) > 0

    def __del__(self):
        self.conn.close()
