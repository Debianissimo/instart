# stuck ci sei?
# bruh eri read-only anche avevo attivato il read-write ... . ... ............  . ... . . . .. . . .. . . .-:_. -:_ :- :-: _: _:_ :_.. . -. .-: ._: ._:
# che si va vincy v
# sera atomino atomoso
# sera vincy vincyoso ok no lol
# dobbiamo fare in modo da mettere i pulsanti in basso
# entra nel vnc
# sei dentro [Y/n]? Sy
# aspe mi dissocio
# # giusto hai ragione, premendo invio è la opzione di defaccio quando faccio apt install
# allora, mentre il prova.py funziona come dovrebbe instart non lo fa, E NON CAPISCO PERCHè DATO CHE HO DATO TUTTI GLI ATTR NECESSARI AL LAYOUT DEI PULSNADI
# idk
import asyncio
import aiohttp
import signal
import functools
import random
import sys

import qasync
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QSizePolicy
from qasync import asyncSlot
import json
from websocket._exceptions import WebSocketConnectionClosedException
from base64 import b64encode
from .client import BackendClient

loop = asyncio.get_event_loop()


class QApplication(QtWidgets.QApplication):
    def __init__(self, qargs: list = None, *args, **kwargs):
        super().__init__(qargs or sys.argv, *args, **kwargs)
        self.loop = loop


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.connected = False
        self.loop = loop
        self.loading_anim = QtWidgets.QLabel()
        self.loading = QtGui.QMovie("/home/ordissimo/instart/assets/placeholder.gif")
        self.loading.setSpeed(500)
        self.loading_anim.setMovie(self.loading)

        # ehm vedi che è onasrt
        # se vai a leggere nel video sta scritto Oansrt
        # la mia infanzia rovinata in una frase
        # Fù
        # FùCk
        self.hellos = [
            "Oansrt!",
            "BIENVENUE, SEMO IN FRANCE SIGNORI!",
            "Buonasera!",
            "OUI!",
        ]
        self.backend = BackendClient(wg=self)
        self.backend.start()
        self.mainlayout = QtWidgets.QVBoxLayout(self)
        self.qlayout = QtWidgets.QGridLayout()

        self.nextbutton = QtWidgets.QPushButton("Inizia ›")
        self.backbutton = QtWidgets.QPushButton("‹ Indietro")
        font = QtGui.QFont()
        font.setPointSize(14)
        self.nextbutton.setGeometry(QtCore.QRect(1040, 1010, 88, 34))
        self.backbutton.setGeometry(QtCore.QRect(1040, 1010, 88, 34))
        self.policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.policy.setHorizontalStretch(0)
        self.policy.setVerticalStretch(0)
        self.policy.setHeightForWidth(self.nextbutton.sizePolicy().hasHeightForWidth())
        self.nextbutton.setSizePolicy(self.policy)
        self.backbutton.setSizePolicy(self.policy)
        self.hello = random.choice(self.hellos)
        self.text = QtWidgets.QLabel(
            f"{self.hello}\n"
            "Benvenuto in Debianissimo!\n"
            "Qui puoi installare Ordissimo OS sul tuo computer!\n"
            "Per iniziare, clicca sul pulsante Inizia qui sotto.",
            alignment=QtCore.Qt.AlignCenter,
        )
        self.qlayout.addWidget(self.text)

        self.nextbutton.clicked.connect(self.nextStep)

        self.title = QtWidgets.QLabel("Scegli una lingua")

        self.title.setSizePolicy(self.policy)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.title.setFont(font)
        self.title.setWordWrap(True)
        self.subtitle = QtWidgets.QLabel(
            "Scegli una lingua tra quelle qui sotto.\n"
            "Attenzione: Dato che è Ordissimo, basta un click sull'opzione per procedere."
        )

        self.buttonslayout = QtWidgets.QHBoxLayout()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subtitle.sizePolicy().hasHeightForWidth())
        self.subtitle.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.subtitle.setFont(font)
        self.subtitle.setWordWrap(True)
        self.label_3 = QtWidgets.QLabel(
            'Ora inserisci la password dell\'utente che verrà creato. Quella predefinita è "ordissimo"'
        )
        self.label_3.setFont(font)
        self.label_4 = QtWidgets.QLabel("Ora inserisci il nome utente Linux.")
        self.label_4.setFont(font)
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setFont(font)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.listWidget.itemClicked.connect(self.setLanguage)
        self.lingue = {}
        self.stepsDone = -2
        self.fullnameEdit = QtWidgets.QLineEdit("Ordissimo")
        self.usernameEdit = QtWidgets.QLineEdit("ordissimo")
        self.passwordEdit = QtWidgets.QLineEdit("ordissimo")
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.spacer = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.text.setFont(font)

        self.buttonslayout.addWidget(self.nextbutton, alignment=QtCore.Qt.AlignRight)
        self.mainlayout.addLayout(self.qlayout)
        self.mainlayout.addLayout(self.buttonslayout)
        self.fullnameEdit.textChanged.connect(self.updateUsername)
        self.fullnameEdit.setClearButtonEnabled(True)
        self.usernameEdit.textChanged.connect(self.enableNextButtonOnUsernameOrPassword)
        self.passwordEdit.textChanged.connect(self.enableNextButtonOnUsernameOrPassword)

    def enableNextButtonOnUsernameOrPassword(self, _):
        self.nextbutton.setEnabled(
            bool(self.usernameEdit.text() and self.passwordEdit.text())
        )

    def updateUsername(self, fullname):
        username = "ordissimo"
        if fullname:
            username = fullname.strip().split()[0].replace("'", "").lower()

        self.usernameEdit.setText(username)

    @asyncSlot()
    async def setUser(self):
        self.nextbutton.clicked.connect(self.nextStep)

        fullname = self.fullnameEdit.text()
        username = self.usernameEdit.text()
        password = b64encode(self.passwordEdit.text().encode())
        self.startLoading()
        await self.backend.send(
            user_fullname=fullname, username=username, password=password.decode()
        )
        self.onlyStopLoading()
        await self.nextStep()

    @asyncSlot()
    async def setLanguage(self, che):
        keys = list(self.lingue.keys())
        curr = self.listWidget.currentRow()
        self.startLoading()
        await self.backend.send(language=keys[curr])
        self.onlyStopLoading()
        await self.nextStep()

    async def moveToUsers(self):
        self.nextbutton.clicked.connect(self.setUser)
        self.qlayout.addWidget(self.title)
        self.qlayout.addWidget(self.subtitle)
        self.title.show()
        self.subtitle.show()
        self.qlayout.addWidget(self.fullnameEdit)
        self.qlayout.removeWidget(self.listWidget)
        self.qlayout.addWidget(self.label_4)
        self.qlayout.addWidget(self.usernameEdit)
        self.qlayout.addWidget(self.label_3)
        self.qlayout.addWidget(self.passwordEdit)

        self.title.setText("Imposta gli utenti")
        self.subtitle.setText(
            "Per poter usare Debianissimo, è necessario almeno un utente "
            "(dato che non puoi nemmeno loggare da root perchè quelli "
            "di Ordissimo sono marsi e cambiano password). Scegli il nome completo dell'utente."
        )
        self.qlayout.addItem(self.spacer)

        self.buttonslayout.addWidget(self.backbutton, alignment=QtCore.Qt.AlignLeft)
        self.buttonslayout.addWidget(self.nextbutton, alignment=QtCore.Qt.AlignRight)
        self.nextbutton.show()

    async def moveToLanguages(self):

        self.startLoading()
        self.lingue: dict = json.loads(await self.backend.send("languages"))

        for i in range(len(self.lingue)):
            QtWidgets.QListWidgetItem(self.listWidget)

        for i, lingua in enumerate(self.lingue.values()):
            self.listWidget.item(i).setText(lingua)

        self.onlyStopLoading()

        self.qlayout.addWidget(self.title)
        self.title.show()
        self.qlayout.addWidget(self.subtitle)
        self.subtitle.show()
        self.qlayout.addWidget(self.listWidget)
        self.listWidget.show()

    def startLoading(self):
        wgts = [self.title, self.subtitle, self.listWidget, self.text, self.nextbutton]
        for wgt in wgts:
            wgt: QtWidgets.QWidget
            self.qlayout.removeWidget(wgt)
            wgt.hide()
        self.mainlayout.addWidget(self.loading_anim, alignment=QtCore.Qt.AlignCenter)
        self.loading_anim.show()
        self.loading.start()

    def onlyStopLoading(self):
        self.loading.stop()
        self.mainlayout.removeWidget(self.loading_anim)
        self.loading_anim.hide()

    @asyncSlot()
    async def nextStep(self):  # ora lo cambio in modo che vada sul coso
        # self.text.setText(random.choice(self.hello))
        # self.text.setText("muso marso devi aspettare la risposta..")
        if self.stepsDone == -2:
            while not self.connected:
                self.nextbutton.setEnabled(False)
                self.text.setText(f"{self.hello}\n"
                "Benvenuto in Debianissimo!\n"
                "Qui puoi installare Ordissimo OS sul tuo computer!\n"
                "Per iniziare, connettiti ad Internet dal pulsante "
                "che trovi nella barra qui sotto.")
                await asyncio.sleep(0)
            else:
                self.nextbutton.setEnabled(True)
                self.text.setText(f"{self.hello}\n"
                "Benvenuto in Debianissimo!\n"
                "Qui puoi installare Ordissimo OS sul tuo computer!\n"
                "Per iniziare, clicca sul pulsante Inizia qui sotto.")
                self.connected = True
        self.startLoading()
        status = await self.backend.send("status")
        while status != "ready":
            status = await self.backend.send("start")

        self.onlyStopLoading()
        self.nextbutton.setText("Avanti ›")
        self.stepsDone += 1
        if self.stepsDone == -1:
            await self.moveToLanguages()
        elif self.stepsDone == 0:
            await self.moveToUsers()
            self.stepsDone += 0.5
        elif self.stepsDone == 0.5:
            await self.setUser()

        # ho sminchiato tutto come al solito :D ah si guarda che range ha due proprietà
        # ne va bene anche una ah giusto
        # non fa più nulla il pulsante taca :NEUTE neute neute neute
        # perché lasci i commenti belli


async def main():
    _connection_error = None
    loop = asyncio.get_event_loop()
    future = asyncio.Future()

    def close_future():
        loop.call_later(10, future.cancel)
        future.cancel()

    app = QtWidgets.QApplication.instance()
    mainWindow = MyWidget()
    mainWindow.show()
    async with aiohttp.ClientSession(loop=loop) as session:
        try:
            await session.get("https://google.com")
        except Exception as e:
            _connection_error = e

    mainWindow.connected = _connection_error is None


    def handle_close(*args):
        """Handler for the SIGINT signal."""
        try:
            mainWindow.backend.ws.send("close")

            while mainWindow.backend._last_arrived_message == None:
                pass
            mainWindow.backend.ws.close()
        except WebSocketConnectionClosedException:
            pass
        app.quit()

    signal.signal(signal.SIGINT, handle_close)
    signal.signal(signal.SIGTERM, handle_close)
    timer = QtCore.QTimer()
    timer.start(0)
    timer.timeout.connect(lambda: None)

    if hasattr(app, "aboutToQuit"):
        app.aboutToQuit.connect(close_future)

    await future

    return True


def start():
    try:
        qasync.run(main())
    except asyncio.CancelledError:
        pass
