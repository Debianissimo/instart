import os


def instart():
    from . import frontend

    frontend.start()


def launch_backend():
    if os.geteuid() != 0:
        raise RuntimeError("IL backend deve essere avviato da root :NEUTE")
    from . import backend

    backend.start()
