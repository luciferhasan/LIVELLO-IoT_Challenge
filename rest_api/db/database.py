import sqlite3
import os

DB_PATH = os.getenv('DB_PATH')
if DB_PATH is None:
    DB_PATH = '/home/user/Documents/LIVELLO-IoT-Challenge/data/events.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # to return dict-like rows
    return conn
