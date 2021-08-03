import os
from setuptools import setup

if os.geteuid() != 0:
    raise RuntimeError("Questo script deve essere avviato da root :NEUTE")

res = os.system("apt install python3-apt parted")
if res != 0:
    raise RuntimeError(f"L'installazione dei pacchetti ha dato un errore {res}.")

res = os.system("cp ./instart.desktop /usr/share/applications/instart.desktop")
if res != 0:
    raise RuntimeError(f"La copia dei file necessari ha dato un errore {res}")

if os.getcwd() != "/usr/share/instart":
    if not os.getcwd().endswith("instart"):
        raise NameError(
            'Devi essere nella cartella di lavoro, e deve chiamarsi "instart".'
        )

    res = os.system(
        f"rm -f /usr/share/instart; ln -sf {os.getcwd()} /usr/share/instart"
    )
    if res != 0:
        raise RuntimeError(
            "Non sono riuscito a creare un symlink che punta a /usr/share/instart. Prova a installare il modulo da quella cartella."
        )

requirements = [
    "pyside2==5.14.2.3",
    "sanic",
    "websocket-client",
    "python-box",
    "qasync",
    "hurry.filesize",
    "pyparted",
]

setup(
    name="instart",
    version="1.0",
    author="Vincy.exe",
    author_email="contatta@debianissimo.it",
    description="L'installer di Debianissimo",
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points="""\
[console_scripts]
instart = instart:instart
""",
)
