import asyncio
import websockets
import json
from PySide2 import QtCore
from threading import Event
from websocket._abnf import ABNF
from functools import partial
from qasync import asyncSlot

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

# dove prendi i json per le risposte? da quel on_message?
# yessete, quel on_message viene invocato quando riceve i mesaggi
# metto un print che capisco che valore ha ah ok
# darebbe <function blah blah blah>


class BackendClient:
    def __init__(self, wg=None):
        self._waiting = False
        self.ws = None
        self._ready = Event()
        self.wg = wg
        self.loop = self.wg.loop

        # websocket.enableTrace(True)
        # self.ws = WebSocketApp( # mh
        #    "ws://localhost:7835/backend",
        #    #on_message=self.on_message, # 🐟 #TUNA
        # )
        # print(self.ws) # cosa returna? se lo sai, ok una classe direi
        # una classe ofc

    def wait_until_ready(self):
        self._ready.wait()

    # COSE STO DUMMY 1?! BOH
    # mo faccio l'issue su github
    # quindi per ora che si fa? (e cmq credo sia un problema di py 3.7 per qualche motivo)
    # sto provando a togliere il QThread e fare in modo che si avvii dallo script iniziale
    async def run(self):
        self.ws = await websockets.connect("ws://localhost:7835/backend")

    def on_ready(self):
        self._ready.set()

    # scusi vincy qua non va asyncSlot() dato che e una funzione async? no perchè questa funzione viene runnata soltanto da me, l'asyncSlot va nei posti dove devo runnarlo ok
    async def send(self, message=None, *args, **kwargs):  # MI COMMUOVO, FUNZIONA
        # ah shit, here we go again
        while self._waiting:
            await asyncio.sleep(0)
        else:
            await asyncio.sleep(0.01)
        if message == None:
            message = kwargs

        if isinstance(message, dict):
            message = json.dumps(
                message
            )  # scusi ma se devi passare da string (che credo sia str) a dict non e loads? oppure non ho capito un cpp?
            # non hai capito un c# perfetto!
            # dumps converte dict a str ah ok
            # per inviare i dati al backend
        # print(f"2, {message}") # e direi che qua li manda giusto? si
        # MA ORA NON VA DI NUOVO
        # è MARSO FORTE
        # cosa ti scrive il programma?
        print(f"^ - {message}")
        await self.ws.send(message, *args)

        self._waiting = True
        data = await self.ws.recv()
        self._waiting = False

        print(f"v - {data}")

        return data

        # while coso.lol == None:
        #    #print(f":neute {self._lasst_arrived_message}") # EMH
        #    await asyncio.sleep(0)
        # else:
        #    msg = self._last_arrived_message
        #    self._last_arrived_message = None

        # await asyncio.sleep(0.5) # sè
        # print(f"3, {msg}") # quindi qua riceve i messaggi dal backend ma non abbiamo salvato
        # qualcuno ci dia la medaglia per i mona
        # sto punto direi che il problema e che riceve 2 messaggi perche negli altri non arriva { result: "done", errors: [] }
        # puà essere
        # puà(to)?
        # LMFAOOOOOO
        # if "result" in msg: return
        # print(f"4, returned {msg}")  #abbiam capito che flyni è vivo 🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟 lmao
        # posso vedere il risultato di 4? scusi ma si e bloccato il terminale remoto o solo io vedo ancora i messaggi di quando c'era il print nel while?
        # non ho ancora avviato ok
        # vai pure
        # sto giro ha dato i settori (credo siano settori)
        # cosa dice in GUI? DISCKORD letto
        # riavvia che vediamo solo con il print del 4
        # ha returnato giusto
        # mo provemo senza
        # pronti ai [] e done
        # ok mo sono confuso
        # cerchiamo il print colpevole
        # io direi troppi commenti lmfaso
        # mhhh
        # io aggiungerei piu tuna pero :)
        # 🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟🐟
        # looooooooooooooooooooooooool
        # ma perche returna doppio se lo sai? (anche se direi di no se non starei sclerando)
        # perchè manda la config degli utenti e subito dopo chiede le partizioni, quindi si confondono
        # e mettere un asyncio.sleep(0.4)? (o anche meno)
        # l'ho messo da 0.1 in un altro file ok penso sia questione di ms se un print puo "sistemare"
        # a
        # perche un print penso ci metta 10 ms manco
        # ma cosa le dice la GUI al momento?
        # nope
        # perfetto (ironia se non si fosse capito)
        # a mo va
        # dopo aver messo sto asyncio.sleep() qua sotto?
        # se si, prova a levare quello nell'altro file e vedem che succede
        # lo avevo già tolto dall'altro file
        # FUNZIONAAAA
        # ok mo vogliamo diverci ad abbassare il piu possibile sto valore?
        # fatto
        # ora 0.2
        # await asyncio.sleep(0.001) # questo valore intendo, e a 1 ms, direi che va bene si, quindi mo retruna correttamente sempre i settori (credo siano settori)? FESTAAAAA, funziona
        # non è vero non funziona niente
