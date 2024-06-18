
import sqlite3
import os


class Database:
    database_file = os.path.join(
        os.path.dirname(__file__), 'zoomai_database.db')

    def __init__(self, dpath=database_file):

        if not os.path.exists(dpath):
            os.mknod(dpath)

        self.conn = sqlite3.connect(dpath)
        self.cursor = self.conn.cursor()

        self.create_db() if not self.tables_exist() else None

    def create_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, created_at TEXT, prompts TEXT, ready INTEGER)
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, image BLOB,  image_order INTEGER ,FOREIGN KEY(project_id) REFERENCES projects(id))
        ''')

        self.conn.commit()

        print('database created')
    
    def get_project_count(self):

        self.cursor.execute('''
            SELECT COUNT(*) FROM projects
        ''')

        count = self.cursor.fetchone()[0]

        return count
    
    def delete_project(self, p_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
            DELETE FROM images WHERE project_id = ?
            ''', (p_id,))
            
            cursor.execute('''
            DELETE FROM projects WHERE id = ?
            ''', (p_id,))
            
            self.conn.commit()
            print("Project and associated images deleted successfully.")
        except Exception as e:
            self.conn.rollback()
            print(f"An error occurred: {e}")
        finally:
            cursor.close()

    def insert_project(self, name, created_at, prompts):
        self.cursor.execute('''
            INSERT INTO projects (name, created_at, prompts, ready) VALUES (?, ?, ?, 0)
        ''', (name, created_at, prompts))

        self.conn.commit()

        return self.cursor.lastrowid
    
    # def insert_project_cover(self, project_id, cover):
    #     self.cursor.execute('''
    #         UPDATE projects SET cover = ? WHERE id = ?
    #     ''', (sqlite3.Binary(cover), project_id))

    #     self.conn.commit()

    def insert_image(self, project_id, image, image_order):
        self.cursor.execute('''
            INSERT INTO images (project_id, image, image_order) VALUES (?, ?, ?)
        ''', (project_id, sqlite3.Binary(image), image_order))

        self.conn.commit()
    
    def update_ready(self, project_id):
        self.cursor.execute('''
            UPDATE projects SET ready = 1 WHERE id = ?
        ''', (project_id,))
        self.conn.commit()


    def get_all_projects(self):
        self.cursor.execute('''
            SELECT projects.id, projects.name, images.image, projects.ready
            FROM projects
            LEFT JOIN (
                SELECT project_id, image FROM images
                WHERE image_order = 0
            ) images
            ON projects.id = images.project_id      
        ''')

        projects_with_images = {}
        rows = self.cursor.fetchall()
        for row in rows:
            project_id = row[0]
            if project_id not in projects_with_images:
                projects_with_images[project_id] = {
                    'id': project_id,
                    'name': row[1],
                    'cover': row[2],
                    'ready': row[3]
                }
        return projects_with_images

    def get_images(self, project_id):
        self.cursor.execute('''
            SELECT image FROM images WHERE project_id = ? ORDER BY image_order DESC
        ''', (project_id,))

        images = self.cursor.fetchall()
        images = [image[0] for image in images]

        return images

    def get_images_ids(self):
        self.cursor.execute('''
            SELECT DISTINCT project_id FROM images ORDER BY project_id
        ''')

        projects = self.cursor.fetchall()

        return projects

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
