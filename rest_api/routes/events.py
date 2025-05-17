from fastapi import APIRouter
from db.database import get_db_connection
from models.schemas import Event

router = APIRouter()

@router.get("/devices/{device_id}/events", response_model=list[Event])
def get_device_events(device_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE device_id = ? ORDER BY timestamp DESC LIMIT 10", (device_id,))
    events = cursor.fetchall()
    conn.close()
    return [dict(e) for e in events]
