from fastapi import APIRouter
from db.database import get_db_connection
from models.schemas import Device

router = APIRouter()

@router.get("/devices", response_model=list[Device])
def get_devices():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM devices")
    devices = cursor.fetchall()
    conn.close()
    return [dict(d) for d in devices]
