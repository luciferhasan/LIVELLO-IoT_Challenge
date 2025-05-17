import sqlite3
import os
from eventSchema import DeviceEvent

DB_PATH = os.getenv('DB_PATH')
if DB_PATH is None:
    DB_PATH = '/home/user/Documents/LIVELLO-IoT-Challenge/data/events.db'

# Setup database and tables if not exists
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            device_id TEXT PRIMARY KEY,
            last_seen TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT,
            sensor_type TEXT,
            sensor_value REAL,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(event):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insert into events table
    cursor.execute('''
        INSERT INTO events (device_id, sensor_type, sensor_value, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (event.device_id, event.sensor_type, event.sensor_value, event.timestamp))

    # Insert or update into devices table
    cursor.execute('''
        INSERT INTO devices (device_id, last_seen)
        VALUES (?, ?)
        ON CONFLICT(device_id) DO UPDATE SET last_seen=excluded.last_seen
    ''', (event.device_id, event.timestamp))

    conn.commit()
    conn.close()
