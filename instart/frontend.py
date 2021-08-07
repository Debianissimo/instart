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
import traceback
import aiohttp
import signal
import random

import qasync
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QSizePolicy
from qasync import asyncSlot
from base64 import b64encode
from hurry.filesize import size, alternative as alternative_size_system
from .backend import Backend


class MyWidget(QtWidgets.QWidget):
    def __init__(self, loop):
        super().__init__()
        self.resize(512, 512)
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
        self.backend = Backend(loop)
        self.mainlayout = QtWidgets.QVBoxLayout(self)
        self.qlayout = QtWidgets.QGridLayout()
        self._ready = False
        self.nextbutton = QtWidgets.QPushButton("Inizia ›")
        self.backbutton = QtWidgets.QPushButton("‹ Indietro")
        font = QtGui.QFont()
        font.setPointSize(14)
        self.nextbutton.setGeometry(QtCore.QRect(1040, 1010, 88, 34))
        self.backbutton.setGeometry(QtCore.QRect(1040, 1010, 88, 34))  # noicre
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
        self.backbutton.clicked.connect(self.prevStep)

        self.title = QtWidgets.QLabel(alignment=QtCore.Qt.AlignLeft)

        # self.title.setSizePolicy(self.policy)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.title.setFont(font)
        self.title.setWordWrap(True)
        self.subtitle = QtWidgets.QLabel(
            alignment=QtCore.Qt.AlignLeft,
        )

        self.buttonslayout = QtWidgets.QHBoxLayout()
        self.subtitlePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        self.subtitlePolicy.setHorizontalStretch(0)
        self.subtitlePolicy.setVerticalStretch(0)
        self.subtitlePolicy.setHeightForWidth(
            self.subtitle.sizePolicy().hasHeightForWidth()
        )
        self.subtitle.setSizePolicy(self.subtitlePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.subtitle.setFont(font)
        self.subtitle.setWordWrap(True)
        self.label_3 = QtWidgets.QLabel(
            'Ora inserisci la password dell\'utente che verrà creato. Quella predefinita è "ordissimo"'
        )  # dove mettiamo?
        self.label_3.setFont(font)
        self.label_4 = QtWidgets.QLabel("Ora inserisci il nome utente Linux.")
        self.label_4.setFont(font)
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setFont(font)
        QtCore.QMetaObject.connectSlotsByName(self)
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
        self.progressBar = QtWidgets.QProgressBar()
        barFont = QtGui.QFont()
        barFont.setPointSize(10)
        barFont.setWeight(75)
        barFont.setBold(True)
        self.progressBar.setFont(barFont)
        self.subProgressText = QtWidgets.QLabel()
        self.subProgressText.setFont(font)
        self.subProgressText.setWordWrap(True)
        self.progressBar.setFormat("Progresso: %p%")

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
        self.startLoading()

        fullname = self.fullnameEdit.text()
        username = self.usernameEdit.text()
        password = b64encode(self.passwordEdit.text().encode())
        self.backend.user_fullname = fullname
        self.backend.username = username
        self.backend.password = password.decode()  # mo va...
        self.onlyStopLoading()
        self.nextbutton.clicked.disconnect()
        self.nextbutton.clicked.connect(self.nextStep)
        await self.nextStep()
        # await self.nextStep()
        # self.stepsDone -= (
        #    0.5  # mezzo step? # si perchè mezzo sarebbe la seconda metà dello step
        # )
        # praticamente ho messo che per impostare l'utente vada di mezzo step perchè così quando fa il nextStep va a dire al backend la configurazione e poi va avanti

    @asyncSlot()
    async def setLanguage(self, che):
        keys = list(self.backend.languages.keys())
        curr = self.listWidget.currentRow()
        self.backend.language = keys[curr]
        await self.nextStep()

    async def moveToUsers(self):
        self.nextbutton.clicked.disconnect()
        self.nextbutton.clicked.connect(self.setUser)
        self.qlayout.addWidget(self.title)
        self.qlayout.addWidget(self.subtitle)
        self.title.show()
        self.subtitle.show()
        self.qlayout.addWidget(self.fullnameEdit)
        self.fullnameEdit.show()
        self.qlayout.removeWidget(self.listWidget)
        self.qlayout.addWidget(self.label_4)
        self.label_4.show()
        self.qlayout.addWidget(self.usernameEdit)
        self.usernameEdit.show()
        self.qlayout.addWidget(self.label_3)
        self.label_3.show()
        self.qlayout.addWidget(self.passwordEdit)
        self.passwordEdit.show()

        self.title.setText("Imposta gli utenti")
        self.subtitle.setText(
            "Per poter usare Debianissimo, è necessario almeno un utente "
            "(dato che non puoi nemmeno loggare da root perchè quelli "
            "di Ordissimo sono marsi e cambiano password). Scegli il nome completo dell'utente."
        )
        self.qlayout.addItem(self.spacer)

        self.buttonslayout.addWidget(self.backbutton, alignment=QtCore.Qt.AlignLeft)
        self.backbutton.show()
        self.buttonslayout.addWidget(self.nextbutton, alignment=QtCore.Qt.AlignRight)
        self.nextbutton.show()

    async def moveToLanguages(self):

        self.startLoading()
        try:
            self.listWidget.itemClicked.disconnect()
        except RuntimeError:
            pass
        self.listWidget.itemClicked.connect(self.setLanguage)

        self.listWidget.clear()

        for i, lingua in enumerate(self.backend.languages.values()):
            QtWidgets.QListWidgetItem(self.listWidget)
            self.listWidget.item(i).setText(lingua)

        self.onlyStopLoading()
        # questo è movetolanguages non movetopartitions
        # sono un mona seriale
        self.qlayout.addWidget(self.title)
        self.title.show()
        self.qlayout.addWidget(self.subtitle)
        self.subtitle.show()
        self.qlayout.addWidget(self.listWidget)
        self.listWidget.show()

    @asyncSlot()
    async def setDisk(self):
        self.nextbutton.clicked.disconnect()
        self.nextbutton.clicked.connect(self.nextStep)
        keys = list(self.disks.keys())
        curr = self.listWidget.currentRow()
        self.backend.disk = f"/dev/{keys[curr]}"
        await self.installSystem()

    @asyncSlot()
    async def installSystem(self):
        self.startLoading()
        self.title.setText("Installazione del sistema...")
        self.subtitle.setText(
            "Sto installando il sistema Ordissimo con gli strumenti Debianissimo. "
            "Potrebbe volerci un po' visto che sto installando anche i pacchetti "
            "che puoi trovare nello store."
        )
        self.onlyStopLoading()
        self.qlayout.addWidget(self.title)
        self.title.show()
        self.qlayout.addWidget(self.subtitle)
        self.subtitle.show()
        self.qlayout.addWidget(self.progressBar)
        self.progressBar.show()
        self.qlayout.addWidget(self.subProgressText)
        self.subProgressText.show()
        self.qlayout.addItem(self.spacer)
        await self.backend.install(self.progressBar, self.subProgressText)

    @asyncSlot()
    async def confirmDiskChoice(self, wat):
        self.startLoading()
        self.onlyStopLoading()
        self.nextbutton.clicked.disconnect()
        self.nextbutton.clicked.connect(self.setDisk)
        self.backbutton.clicked.disconnect()
        self.backbutton.clicked.connect(self.moveToPartitions)
        self.title.setText("Sei sicuro?")
        self.subtitle.setText(
            "Sei sicuro di aver scelto il disco giusto? Il disco selezionato verrà formattato, "
            "quindi, dopo questa operazione, perderai TUTTI i dati presenti su quel disco!\n"
            "Noi non ci assumiamo alcuna responsabilità di quello che fai. Il tuo computer è il tuo computer."
        )
        self.backbutton.setText("‹ No")
        self.nextbutton.setText("Sì ›")

        self.qlayout.addWidget(self.title)
        self.title.show()
        self.qlayout.addWidget(self.subtitle)
        self.subtitle.show()
        self.qlayout.addItem(self.spacer)
        self.buttonslayout.addWidget(self.backbutton, alignment=QtCore.Qt.AlignLeft)
        self.backbutton.show()
        self.buttonslayout.addWidget(self.nextbutton, alignment=QtCore.Qt.AlignRight)
        self.nextbutton.show()

    @asyncSlot()
    async def moveToPartitions(self):
        try:
            self.listWidget.itemClicked.disconnect()
        except RuntimeError:
            pass
        self.listWidget.itemClicked.connect(self.confirmDiskChoice)
        self.backbutton.clicked.disconnect()
        self.backbutton.clicked.connect(self.prevStep)
        self.startLoading()
        self.disks: dict = await self.backend.disks()

        self.title.setText("Scegli il disco")
        self.subtitle.setText(
            "Ora, scegli il disco dove installare Debianissimo. Il disco deve avere almeno 64GB.\n"
            "ATTENZIONE: Non puoi creare una partizione specifica per Debianissimo. "
            "Puoi solo usare un intero disco. Motivo? Chiedi ad Ordissimo! Nemmeno noi Developerissimi lo sappiamo. "  # se usavamo la mia frase andava fuori dallo schermo #esatto
            "Pertanto, il dualboot non è supportato.\n"
            # f"Io chicchi voglio sapere il json, ecco perchè a tradimento metto sta cosa {self.disks} ma lol"
        )
        self.listWidget.clear()

        for i, prop in enumerate(self.disks.items()):
            QtWidgets.QListWidgetItem(self.listWidget)
            nome, grandezza = prop
            # if nome in ["result", "errors"] and grandezza in ["done", []]:
            #    # in qualche modo si sono swappate le richieste del setup utenti e del partizionamento, si riprova
            #    self.disks = json.loads(await self.backend.send("disks"))
            #    return await marso()

            # if not type(grandezza) == "int":
            #    continue # mi dicono che il check forse funziona ma tutti dischi apprentemente sono string, ok mo sono confuso

            if (
                grandezza < 64000000000
            ):  # ho messo un int() EH # DI NUOVO AAAAAA MA SCIOPA, proviamo senza int, non ho salvato ops vedem se converto a string e poi integrer # non credo manco io
                # ah mo ho capito, gradetta = 'done'  NO NON DI NUOVO
                # scusi posso chiedere l'utilita di sto if? che dice se grandezza minore di 64 GB continua se no ignora lo statament
                # è comploicato da spiegare
                continue

            grandezza = size(grandezza, alternative_size_system)
            self.listWidget.item(i).setText(f"{nome} - Disco {i} da {grandezza}")
            # if nome == "sda":
            #    self.listWidget.item(i).setHidden(True)

        self.onlyStopLoading()
        self.qlayout.addWidget(self.title)
        self.title.show()
        self.qlayout.addWidget(self.subtitle)
        self.subtitle.show()
        self.qlayout.addWidget(self.listWidget)  # si sono un riutilizzatore di widget
        self.listWidget.show()
        # self.qlayout.addWidget(self.backbutton)
        # self.backbutton.show()

        # VEENCY EXPOSD, non è super
        # dovrei cambiare l'username di github
        # si, vincynonsuper
        # :neute intendevo a Vincy.exe o Vincydotexe, oppure (come ho fatto al VNC) Vincy dot exe.
        # VNCdotelf
        # per farti capire che intendo, https://use-fasmga-or.go-get-a.life/54f8Sq8nH questo è il mio account su realvnc
        # perchè voleva il cognome e allora ho messo "dot exe."
        # su google ho come cognome -
        # lol
        # che si fa?
        # /midissocio

    def startLoading(self):
        wgts = [
            self.title,
            self.subtitle,
            self.listWidget,
            self.text,
            self.nextbutton,
            self.usernameEdit,
            self.fullnameEdit,
            self.passwordEdit,
            self.label_3,
            self.label_4,
            self.backbutton,
        ]  # usiamo il coso chat # non ho capito session chat di ls #a ok
        itms = [self.spacer]
        for wgt in wgts:
            wgt: QtWidgets.QWidget
            self.qlayout.removeWidget(wgt)
            wgt.hide()

        for itm in itms:
            self.qlayout.removeItem(itm)

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
        self.startLoading()
        self.backbutton.setText("‹ Indietro")
        self.nextbutton.setText("Avanti ›")
        if self.stepsDone == -2:
            while not self.connected:
                self.nextbutton.setEnabled(False)
                self.text.setText(
                    f"{self.hello}\n"
                    "Benvenuto in Debianissimo!\n"
                    "Qui puoi installare Ordissimo OS sul tuo computer!\n"
                    "Per iniziare, connettiti ad Internet dal pulsante "
                    "che trovi nella barra qui sotto."
                )
                await asyncio.sleep(0)
            else:
                self.nextbutton.setEnabled(True)
                self.text.setText(
                    f"{self.hello}\n"
                    "Benvenuto in Debianissimo!\n"
                    "Qui puoi installare Ordissimo OS sul tuo computer!\n"
                    "Per iniziare, clicca sul pulsante Inizia qui sotto."
                )
                self.connected = True

        self.onlyStopLoading()

        self.stepsDone += 1
        if self.stepsDone == -1:
            # await self.moveToLanguages()
            # elif self.stepsDone == 0:
            #    await self.moveToUsers()
            # elif self.stepsDone == 1:
            await self.moveToPartitions()

        # ho sminchiato tutto come al solito :D ah si guarda che range ha due proprietà
        # ne va bene anche una ah giusto
        # non fa più nulla il pulsante taca :NEUTE neute neute neute
        # perché lasci i commenti belli

    @asyncSlot()
    async def prevStep(self):
        self.backbutton.setText("‹ Indietro")
        self.nextbutton.setText("Avanti ›")
        self.startLoading()
        self.onlyStopLoading()

        self.stepsDone -= 1
        if self.stepsDone == -1:
            await self.moveToLanguages()
        elif self.stepsDone == 0:
            #    await self.moveToUsers()
            # elif self.stepsDone == 1:
            await self.moveToPartitions()


async def main():
    _connection_error = None
    loop = asyncio.get_event_loop()
    future = loop.create_future()

    async with aiohttp.ClientSession(loop=loop) as session:
        try:
            async with session.get("https://google.com"):
                pass
        except Exception as e:
            print(traceback.format_exc())
            print("marso")
            _connection_error = e

    app = QtWidgets.QApplication.instance()
    mainWindow = MyWidget(loop)
    mainWindow.show()

    mainWindow.connected = _connection_error is None

    def close(*args):
        """Handler for the SIGINT signal."""
        loop.call_later(10, future.cancel)
        future.cancel()
        # try:
        #    for task in asyncio.all_tasks(loop):
        #        task.cancel()
        # except asyncio.CancelledError:
        #   pass
        if not "marso" in args:
            app.quit()
        loop.stop()

    signal.signal(signal.SIGINT, close)
    signal.signal(signal.SIGTERM, close)
    timer = QtCore.QTimer()
    timer.start(0)
    timer.timeout.connect(lambda: None)

    if hasattr(app, "aboutToQuit"):
        app.aboutToQuit.connect(close)

    await future
    # aspetta anche tu il futuro XD
    # LMFAO
    return True


def start():
    try:
        qasync.run(main())
    except asyncio.CancelledError:
        pass
