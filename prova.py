# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui',
# licensing of 'untitled.ui' applies.
#
# Created: Tue Jul  6 18:38:12 2021
#      by: pyside2-uic  running on PySide2 5.11.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class wgt(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel("Imposta gli utenti", self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label.setFont(font)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(
            "Per poter usare Debianissimo, è necessario almeno un utente "
            "(dato che non puoi nemmeno loggare da root perchè "
            "quelli di Ordissimo sono marsi e cambiano password). "
            "Scegli il nome completo dell'utente",
            self,
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit)
        self.label_4 = QtWidgets.QLabel("Ora inserisci il nome utente Linux.", self)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.lineEdit_3 = QtWidgets.QLineEdit(self)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.verticalLayout_2.addWidget(self.lineEdit_3)
        self.label_3 = QtWidgets.QLabel(
            "Ora inserisci la password dell'utente che verrà creato.", self
        )
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.lineEdit_2 = QtWidgets.QLineEdit(self)
        self.lineEdit_2.setInputMask("")
        self.lineEdit_2.setText("")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setPlaceholderText("")
        self.lineEdit_2.setClearButtonEnabled(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_2.addWidget(self.lineEdit_2)
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_2 = QtWidgets.QPushButton("Indeitro", self)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_4.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton("Avanti", self)
        self.pushButton.setEnabled(False)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_4.addWidget(self.pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)


# SERA
# seha buona, seha anche a lei fleny col suo tuna
# lol.
# seha 🐟🐟🐟🐟🐟 (io sui codici saluto con i tuna 😀 )
# sera a tutti i tunafdsgf allpor allora, non posso ne cancellare ne andare a capo
# emh ok...
# ewhm idem ah eccolo apriamo vscode WHY SENZA UTENTE?!
# perche stiamo facendo qualcosa per debianissimo
# che e basato su ordissimo
# che ti deve semplificare la vita
# quindi a chi servono gli utenti!
# OvViAmEnTe nEsSuNo
# stano
# BONA SERA E MO POSSO CANCELLARE YEEEEEE
# grafie per avermi cancellato il messaggio :)
# ma io ho ancora https://en.wikipedia.org/wiki/Zen_of_Python aperto
# cosa devi fare vincy?
# cmq io non vedo il cursore di vincy
# sono qui
# mo lo vedo
# grafie liveshare
# liveshare: prefo
# comunque dovrei capire perchè manda solo alcune cose e poi si ferma
# ora sto cambiando modulo, uso uno già async 🐟🐟🐟🐟🐟
# ok
# si va a vedere la doc
# a ma non siamo nel modulo, siamo nel file sbagliato lmfao


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    def handle_close(*args):
        """Handler for the SIGINT signal."""
        app.quit()

    import signal

    signal.signal(signal.SIGINT, handle_close)
    timer = QtCore.QTimer()
    timer.start(500)  # You may change this if you wish.
    timer.timeout.connect(lambda: None)  # Let the interpreter run each 500 ms.
    widget = wgt()
    widget.show()
    sys.exit(app.exec_())
