from fastapi import FastAPI
from routes import devices, events

app = FastAPI()

app.include_router(devices.router)
app.include_router(events.router)
