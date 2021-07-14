import asyncio
import json
from PySide2 import QtCore
from websocket import WebSocketApp
from threading import Event
from websocket._abnf import ABNF

# sera chicco di caffè
# sera anche a te flyne
# CIAO, SONO LA MARISA :)
# sera
# vuole un po di verdin vomitin spray?
# ok
# credevo stavi per scrivere "vuoi un po' di tuna?" sinceramente
# se vuole ho anche del tuna 🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟
# graziella
# (vedi un mucchio di punti di domanda vero?)
# no, vedo l'emoji del tuna
# ah ok


class BackendClient(QtCore.QThread):
    def __init__(self, parent=None, *, wg=None):
        super().__init__(parent)
        self._ready = Event()
        self.wg = wg
        self._last_arrived_message = None

        # websocket.enableTrace(True)
        self.ws = WebSocketApp(
            "ws://localhost:7835/backend",
            on_message=self.on_message,
        )

    def wait_until_ready(self):
        self._ready.wait()

    def on_ready(self):
        self._ready.set()

    def run(self):
        self.ws.run_forever()

    async def send(self, message=None, *args, **kwargs):
        if message == None:
            message = kwargs

        if isinstance(message, dict):
            message = json.dumps(message)
        self.ws.send(message, *args, opcode=kwargs.pop("opcode", ABNF.OPCODE_TEXT))
        while self._last_arrived_message == None:
            await asyncio.sleep(0)
        else:
            msg = self._last_arrived_message
            self._last_arrived_message = None

        return msg

    def on_message(self, ws, message):
        self._last_arrived_message = message
