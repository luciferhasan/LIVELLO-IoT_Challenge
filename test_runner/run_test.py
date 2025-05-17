import asyncio
import json
import os
import uuid
import webbrowser
import subprocess
from datetime import datetime
from gmqtt import Client as MQTTClient

TOPIC = "/devices/events"
BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "localhost")
ERROR_LOG_PATH = os.getenv("ERROR_LOG_PATH", "../data/error.log")

# Base payload to modify
base_payload = {
    "device_id": "test-device-001",
    "sensor_type": "temperature",
    "sensor_value": 25.0,
    "timestamp": datetime.utcnow().isoformat() + "Z"
}

# Connect gmqtt client
class MQTTTestClient:
    def __init__(self):
        self.client = MQTTClient(f"test-client-{uuid.uuid4()}")
        self.client.on_connect = self.on_connect

    def on_connect(self, client, flags, rc, properties):
        print("Connected to MQTT broker")

    async def connect_and_publish(self, payload):
        await self.client.connect(BROKER_HOST)
        self.client.publish(TOPIC, json.dumps(payload), qos=1)
        await asyncio.sleep(1)
        await self.client.disconnect()

# Tailing the error log in another terminal
def tail_error_log():
    subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"tail -f {ERROR_LOG_PATH}; exec bash"])

# Open Swagger UI
def open_docs():
    webbrowser.open("http://localhost:8000/docs")

# User-driven customization
def customize_payload():
    custom = base_payload.copy()
    print("\n🛠 Customize JSON fields:")
    for key, val in custom.items():
        new_val = input(f"{key} [{val}]: ").strip()
        if new_val:
            if key == "sensor_value":
                try:
                    new_val = float(new_val)
                except:
                    print("Invalid float. Keeping original.")
                    continue
            custom[key] = new_val
    return custom

# Menu
async def main_menu():
    mqtt = MQTTTestClient()

    while True:
        print("\n📡 MQTT Test Menu:")
        print("1. Send valid message")
        print("2. Send malformed message")
        print("3. Customize and send message")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            payload = base_payload.copy()
            payload["timestamp"] = datetime.utcnow().isoformat() + "Z"
            await mqtt.connect_and_publish(payload)

        elif choice == "2":
            bad_payload = "this is not valid json"
            await mqtt.connect_and_publish(bad_payload)

        elif choice == "3":
            custom = customize_payload()
            await mqtt.connect_and_publish(custom)

        elif choice == "4":
            print("✅ Done.")
            break
        else:
            print("❌ Invalid choice.")

# Launch everything
def launch_environment():
    tail_error_log()
    open_docs()

if __name__ == "__main__":
    print("🚀 Starting Test Runner...")
    launch_environment()
    asyncio.run(main_menu())
