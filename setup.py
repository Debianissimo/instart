import os
from setuptools import setup

if os.geteuid() != 0:
    raise RuntimeError("Questo script deve essere avviato da root :NEUTE")

os.popen("cp ./instart.desktop /usr/share/applications/instart.desktop")

requirements = [
    "pyside2==5.14.2.3",
    "sanic",
    "websocket-client",
    "python-box",
    "qasync",
    "hurry.filesize",
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
instart-backend = instart:launch_backend
""",
)
