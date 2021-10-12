# questo script viene avviato quando deve entrare nel chroot per installare roba tipo kernelissimo

import os
import sys
import json
import subprocess
import random
from hurry.filesize import size, alternative

os.environ["DEBIAN_FRONTEND"] = "noninteractive"

os.chroot("/target")

# --- dopo il chroot ---

os.chdir("/")
if os.path.exists("/etc/fstab"):
    os.remove("/etc/fstab")

def do_rm_mtab():
    os.remove("/etc/mtab")

def fake_rm_mtab():
    return

rm_mtab = fake_rm_mtab

if not os.path.exists("/etc/mtab"):
    rm_mtab = do_rm_mtab
    os.system("ln -sf /proc/mounts /etc/mtab")

open("/tmp/marso", "w").write("")
# marso = open("/tmp/marso", "ab")
stdout = sys.stdout
# sys.stdout = marso
# sys.stderr = marso


def sendjson(**kwargs):
    print(json.dumps(kwargs), file=sys.stderr)


"""
# per quando ho bisogno di testàre roba
import time
for i in range(11):
    sendjson(
            text="Download in corso dei pacchetti. mona/marso scaricati. Mancano mona. {pkg}".format(
                pkg="marso{}".format(i)
            ),
            total_bytes=6969696969,
            current_bytes=random.randint(0, 6969696969),
            status="download",
            pkg="marso{}".format(i),
        )
    sendjson(
            text="Download in corso dei pacchetti. mona/marso scaricati. Mancano mona. {pkg}".format(
                pkg="marso{}".format(i)
            ),
            total_bytes=6969696969,
            current_bytes=random.randint(0, 6969696969),
            status="download",
            pkg="marso{}".format(i),
        )
    time.sleep(0.01)

for i in range(10, 101):
    sendjson(
            text="Installazione dei pacchetti. {perc}% installato.".format(perc=i),
            pkg="marso{}".format(i),
            percent=i,
            status="Marsificazione...",
        )
    sendjson(
            text="Installazione dei pacchetti. {perc}% installato.".format(perc=i),
            pkg="marso{}".format(i),
            percent=i,
            status="Marsificazione...",
        )
    time.sleep(0.01)
"""


# '''
subprocess.run(
    "apt update; apt install -y python3-apt wget gnupg python3-pip python-pip-whl=9.0.1-2+deb9u1 python3-setuptools",
    shell=True,
)
subprocess.run("pip3 install -U pip setuptools wheel hurry.filesize", shell=True)

apts = [
    "apt-ordissimo-common_4.1.0_all",
    "apt-ordissimo-common-keyring_4.1.0_all",
    "apt-ordissimo-sr2018_4.1.0_all",
    "apt-ordissimo-sr2018-keyring_4.1.0_all",
]

marsettino = "apt install -y "
for apt_ in apts:
    subprocess.run(
        "wget -O /tmp/{apt}.deb http://substantielwww.dyndns.org/pool/non-free/a/apt-ordissimo/{apt}.deb".format(
            apt=apt_
        ),
        shell=True,
    )
    marsettino += "/tmp/{apt}.deb ".format(apt=apt_)

subprocess.run(marsettino, shell=True)


subprocess.run(
    "wget -qO- http://cdn.debianissimo.it/key.gpg | apt-key add -", shell=True
)


open("/etc/apt/sources.list", "w").write(
    """
deb [arch=amd64] http://substantielwww.dyndns.org sr2018-stable main non-free
deb-src http://substantielwww.dyndns.org          sr2018-stable main non-free
deb [arch=amd64] http://cdn.debianissimo.cf/repos debianissimo  main
# Uncommenta questa repo se vuoi usare i pacchetti dell'archivio Debian.
# ATTENZIONE: Potrebbe rompere il sistema.
#deb [arch=amd64] http://deb.debian.org/debian stretch main non-free contrib
"""
)
os.system("apt update")

import apt
from apt.progress import base


class Progress(base.InstallProgress):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_running = False

    def status_change(self, pkg, percent, status):
        """(Abstract) Called when the APT status changed."""
        perc = round(percent)
        sendjson(
            text="Installazione dei pacchetti. {perc}% installato.".format(perc=perc),
            pkg=pkg,
            percent=percent,
            status=status,
        )


class FProgress(base.AcquireProgress):
    def done(self, item):
        """Invoked when an item is successfully and completely fetched."""
        return self.fetch(item)

    def fetch(self, item):
        current = size(self.current_bytes, alternative)
        fs = size(self.total_bytes - self.current_bytes, alternative)
        total = size(self.total_bytes, alternative)
        sendjson(
            text="Download in corso dei pacchetti. {current}/{total} scaricati. Mancano {fs}. {pkg}".format(
                current=current, total=total, fs=fs, pkg=item.shortdesc
            ),
            total_bytes=self.total_bytes,
            current_bytes=self.current_bytes,
            status="download",
            pkg=item.shortdesc,
        )


cache = apt.Cache()
cache.update()

ordissimo = cache["ordissimo"]
ordissimo.mark_install()
langue = cache["ordissimo-langue-all"]
langue.mark_install()
terminalissimo = cache["terminalissimo"]
terminalissimo.mark_install()
neofetch = cache["neofetch"]
neofetch.mark_install()
prog = Progress()
fprog = FProgress()
cache.commit(install_progress=prog, fetch_progress=fprog)

subprocess.run("lilo", shell=True)
# '''
rm_mtab()
sendjson(status="finished", text="Installazione terminata.")