import websocket
from hurry.filesize import size, alternative
import json

ws = websocket.create_connection("ws://localhost:7835/backend")
ws.send("disks")
for key, value in json.loads(ws.recv()).items():
    print(f"{key}: {size(value, alternative)}")
