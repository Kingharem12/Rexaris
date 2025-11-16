import sqlite3
from .config import DATABASE_FILE
import os

os.makedirs(os.path.dirname(DATABASE_FILE) or '.', exist_ok=True)
conn = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
cur = conn.cursor()

def init_db():
    cur.executescript(open(os.path.join(os.path.dirname(__file__),'schema.sql')).read())
    conn.commit()

def get_conn():
    return conn
