from pydantic import BaseModel, ValidationError, validator
from datetime import datetime

class DeviceEvent(BaseModel):
    device_id: str
    sensor_type: str
    sensor_value: float
    timestamp: str

    # Validate timestamp format is ISO8601
    @validator('timestamp')
    def check_timestamp(cls, v):
        try:
            datetime.fromisoformat(v.replace("Z", "+00:00"))  # support 'Z' as UTC
        except Exception:
            raise ValueError('timestamp must be ISO8601 format')
        return v