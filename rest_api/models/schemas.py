from pydantic import BaseModel

class Device(BaseModel):
    device_id: str
    last_seen: str

class Event(BaseModel):
    event_id: int
    device_id: str
    sensor_type: str
    sensor_value: float
    timestamp: str
