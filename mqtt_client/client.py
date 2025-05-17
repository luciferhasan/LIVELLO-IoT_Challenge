import asyncio
import json
import os
import logging
from gmqtt import Client as MQTTClient
from eventSchema import DeviceEvent, ValidationError
from database import init_db, save_to_db
import uuid


CLIENT_ID = f'iot-client-{uuid.uuid4()}'
print(CLIENT_ID)
STOP = asyncio.Event()

filename = os.getenv('ERROR_FILE_PATH')
print(filename)
if filename is None:
    filename = '/home/user/Documents/LIVELLO-IoT-Challenge/data/error.log'
# Setup logging to a file
logging.basicConfig(
    filename=filename,  # Make sure path exists inside container or use relative path locally
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def on_connect(client, flags, rc, properties):
    print('Connected to MQTT broker')
    client.subscribe('/devices/events')

# Callback: called when client gets message
def on_message(client, topic, payload, qos, properties):
    print(f'Received message on {topic}:')
    try:
        data = json.loads(payload)
        event = DeviceEvent(**data)  # ✅ Schema validation using Pydantic
        print(f"Valid message: {event}")
        save_to_db(event)
    except (json.JSONDecodeError, ValidationError) as e:
        error_msg = f"Invalid message: {payload.decode('utf-8') if isinstance(payload, bytes) else payload}, Error: {e}"
        print(error_msg)
        logging.error(error_msg)

# Callback: on disconnect
def on_disconnect(client, packet, exc=None):
    print('MQTT Client Disconnected')

# Graceful shutdown on SIGINT (Ctrl+C)
def ask_exit(*args):
    STOP.set()

async def main():
    init_db()
    client = MQTTClient(CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    mqtt_host = os.getenv('MQTT_BROKER_HOST')
    print("MQTT Enivron -> ",mqtt_host)
    
    if mqtt_host == 'mqtt-broker':
        mqtt_host = 'mqtt-broker'
    else:
        mqtt_host = 'localhost'
        
    await client.connect(mqtt_host)

    await STOP.wait()
    await client.disconnect()

if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, ask_exit)
    asyncio.run(main())
