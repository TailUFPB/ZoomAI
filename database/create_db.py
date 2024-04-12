import sqlite3
import os

database_path = os.path.join(os.path.dirname(__file__), 'zoomai_database.db')

conn = sqlite3.connect(database_path)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, name TEXT, cover BLOB, created_at TEXT)
''')

cursor.execute('''
     CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY, project_id INTEGER, image BLOB,  image_order INTEGER ,FOREIGN KEY(project_id) REFERENCES projects(id))
''')

conn.commit()
conn.close()