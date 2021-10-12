import asyncio
import json
import os
import subprocess
import pygit2

from functools import partial
from PySide2.QtWidgets import QProgressBar, QLabel, QWidget
from PySide2.QtCore import QTimer
from aiohttp import ClientSession


class PartitionError(Exception):
    pass


class Backend:
    _expected_debootstrap_output = json.load(open("/usr/share/instart/output.json"))

    def __init__(self, widget: QWidget):
        from .frontend import MyWidget

        self.bar: QProgressBar = None
        self.text: QLabel = None
        self.widget: MyWidget = widget
        self.rebootimer: QTimer = widget.rebootimer
        self.loop: asyncio.BaseEventLoop = widget.loop
        # self.languages = {
        #    "en-us": "Inglese (Stati Uniti)",
        #    "it-it": "Italiano",
        #    "be": "Bielorusso",
        #    "ca": "Catalano",
        #    "dz": "Arabo (Algeria)",
        #    "de-de": "Tedesco",
        #    "fr-fr": "Francese",
        #    "lu": "Francese (Lussemburgo)",
        #    "ma": "Arabo (Marocco)",
        #    "nl-nl": "Olandese (Paesi Bassi)",
        #    "es-es": "Spagnolo",
        #    "gb": "Inglese (Regno Unito) (ultimo giusto per fare un dispetto all'Inghilterra, ma per me sarebbe ultimo lo spagnolo :))",
        # }
        # self.language = "en-us"
        # self.user_fullname = "Ordissimo"
        # self.username = "ordissimo"
        # self.password = "b3JkaXNzaW1v"
        self.disk = ""

    async def partition(self):
        efi = os.path.exists("/sys/firmware/efi")
        if efi:
            disks = {
                1: {"label": "root", "path": ""},
                3: {"label": "var", "path": "/var"},
                4: {"label": "secours", "path": "/mnt/secours"},
                5: {"label": "home", "path": "/home"},
            }
        else:
            disks = {
                1: {"label": "root", "path": ""},
                6: {"label": "var", "path": "/var"},
                7: {"label": "secours", "path": "/mnt/secours"},
                8: {"label": "home", "path": "/home"},
            }
        try:
            await self.loop.run_in_executor(
                None, lambda: os.system("sudo umount -Rfl /target; sudo rm -rf /target")
            )
        except Exception:
            pass
        for n, disk in disks.items():
            if (
                await self.loop.run_in_executor(
                    None,
                    lambda: os.system(
                        f"sudo python3 -c 'from instart.partitioning import partition; partition(\"{self.disk}\")'"
                    ),
                )
                != 0
            ):
                raise PartitionError
            await self.loop.run_in_executor(
                None, lambda: os.system(f"sudo mkdir -p /target{disk['path']}")
            )

            for code in [
                await self.loop.run_in_executor(
                    None, lambda: os.system(f"sudo mkfs.ext4 -F {self.disk}{n}")
                ),
                await self.loop.run_in_executor(
                    None,
                    lambda: os.system(f"sudo e2label {self.disk}{n} {disk['label']}"),
                ),
                await self.loop.run_in_executor(
                    None,
                    lambda: os.system(
                        f"sudo mount {self.disk}{n} /target{disk['path']}"
                    ),
                ),
            ]:
                if code != 0:
                    raise PartitionError

        if await self.loop.run_in_executor(
            None,
            lambda: os.system(
                f"sudo mkfs.vfat {self.disk}6"
            ),
        ) != 0:
            raise PartitionError

    async def disks(self):
        disks = [
            a
            for a in (
                await self.loop.run_in_executor(
                    None,
                    lambda: subprocess.run(
                        "sudo lsblk -b -d -o NAME,SIZE",
                        shell=True,
                        capture_output=True,
                    ),
                )
            )
            .stdout.decode()
            .split("\n")
            if "sd" in a
        ]
        result = {}
        for disk in disks:
            result[disk.split()[0]] = int(disk.split()[1])
        return result

    def setProgress(self, progress, text):
        self.text.setText(
            str(text)
        )  # convertito alla classe str in modo che non impazzisca nel caso l'istanza non fosse str
        self.bar.setProperty("value", progress)

    def reboo(*args, **kwargs):
        return subprocess.run("sudo eject -rsfqm; sudo reboot -f", shell=True)

    async def do_update(self, command):
        update = await self.loop.run_in_executor(
            None,
            partial(
                subprocess.Popen,
                command,
                shell=True,
            ),
        )
        poll = update.poll()
        while poll == None:
            await asyncio.sleep(0)
            poll = update.poll()
        else:
            if poll != 0:
                raise ChildProcessError(
                    f"Il tentativo di aggiornamento ha dato codice {poll}."
                )

    async def update(self):
        await self.do_update("sudo git pull")
        await self.do_update("./preupdate.sh")
        await self.do_update("sudo pip3.7 install -Ue .")
        await self.do_update("./postupdate.sh")

    async def checkForUpdates(self):
        coso = await self.loop.run_in_executor(
            None, partial(pygit2.discover_repository, "/usr/share/instart")
        )
        repo = await self.loop.run_in_executor(
            None, partial(pygit2.init_repository, coso)
        )
        id_ = (
            await self.loop.run_in_executor(None, partial(repo.revparse_single, "HEAD"))
        ).id

        async with ClientSession(loop=self.loop) as session:
            async with session.post(
                "http://srv1.jxsterg1.space:8045/check_for_updates",
                json={"id": str(id_)},
            ) as resp:
                has_to_update = await resp.json()
                return has_to_update["has_to_update"]

    async def install(self, bar: QProgressBar, text: QLabel):
        self.bar = bar
        self.text = text

        # formattazione
        # '''
        self.setProgress(0, "Formattazione del disco...")
        try:
            await self.partition()
        except PartitionError:
            self.setProgress(
                3,
                "C'è stato un errore formattando i dischi.\nPer riprovare devi riavviare il sistema live e riavviare l'installazione.",
            )
            return

        self.setProgress(0, "Installazione del sistema base Debian.")
        out = []
        print("a")
        open("/tmp/install.log", "w").write("\n")
        running = await self.loop.run_in_executor(
            None,
            lambda: subprocess.Popen(
                "sudo debootstrap --arch=amd64 --variant=minbase stretch /target http://deb.debian.org/debian | tee -a /tmp/install.log",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ),
        )
        while True:
            out = open("/tmp/install.log").readlines()
            print(len(out) / len(self._expected_debootstrap_output) * 100)
            print(len(out) / len(self._expected_debootstrap_output) * 10)
            line = out[-1].strip()
            if line.startswith("I:"):
                line = line.replace("I:", "", 1).strip()
            await asyncio.sleep(1)
            print(line)
            # out.append(line)
            self.text.setText(f"Installazione del sistema base Debian: {line}")
            percent = (len(out) / len(self._expected_debootstrap_output)) * 10
            print(percent, self.text.text())
            # self.setProgress(sera, marso)
            self.bar.setProperty("value", percent)
            poll = running.poll()
            if (
                # percent >= 10.025316455696203
                # or line
                # == self._expected_debootstrap_output[-1].replace("I:", "", 1).strip()
                poll
                != None
            ):  # cifra completa: 10.025316455696203
                if poll != 0:
                    self.text.setText(
                        "C'è stato un errore. Per riprovare, riavvia il PC."
                    )
                    return
                break
        print("mona")
        code = 0
        # for code in [
        if not os.path.ismount("/target/proc"):
            coso = await self.loop.run_in_executor(
                None,
                lambda: os.system(f"sudo mount -t proc /proc /target/proc"),
            )
            print(coso)
            code += coso

        if not os.path.ismount("/target/dev"):
            coso = await self.loop.run_in_executor(
                None,
                lambda: os.system(f"sudo mount --rbind /dev /target/dev"),
            )
            print(coso)
            code += coso

        if not os.path.ismount("/target/sys"):
            coso = await self.loop.run_in_executor(
                None,
                lambda: os.system(f"sudo mount --rbind /sys /target/sys"),
            )
            print(coso)
            code += coso

        # ]:
        if code != 0:
            for a in range(10):
                self.text.setText("C'è stato un errore. Per riprovare, riavvia il PC.")
            return
        # '''
        insttexxt = "Sto installando i pacchetti Ordissimo"
        self.text.setText(insttexxt + ".")

        postchroot = await self.loop.run_in_executor(
            None,
            lambda: subprocess.Popen(
                "sudo -E python3.5 /usr/share/instart/postchroot.py | tee -a /tmp/install.log",
                shell=True,
                # stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ),
        )
        while True:
            line = postchroot.stderr.readline().decode("UTF-8").strip()
            if line:
                open("/tmp/marsoo", "a").write(f"{line}\n")

            # line = out[-1].strip()
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue

            insttext = insttexxt + f": {data['text']}"

            # {'total_bytes': 1717984132, 'current_bytes': 156248032, 'text': 'Download in corso dei pacchetti. 149 MB/1 GB scaricati. Mancano 1 GB.', 'status': 'download'}
            await asyncio.sleep(0.1)
            self.text.setText(insttext)
            if data["status"] == "download":
                try:
                    perc = round((data["current_bytes"] / data["total_bytes"]) * 10)
                except ZeroDivisionError:
                    pass

                self.bar.setProperty("value", 10 + perc)
            elif data["status"] == "finished":
                break
            else:
                perc = round(data["percent"]) + 20
                if perc >= 50 and (perc - 20) <= 50:
                    perc = 50
                elif perc >= 50 and (perc - 20) >= 50:
                    perc = perc - 20

                if perc >= 100:
                    perc = 100

                self.bar.setProperty("value", perc)

        os.system("sudo umount -Rfl /target")
        self.rebootimer.timeout.connect(lambda: self.reboo)
        self.rebootimer.setProperty("repeat", False)
        self.rebootimer.start(10000)
        self.widget.subProgressText.hide()
        self.widget.title.setText("Riavvio in corso...")
        self.widget.nextbutton.setText("Riavvia ora ›")
        bar.setFormat("")
        remaining = 10000
        while remaining != 0:
            remaining = self.rebootimer.remainingTime()
            percent = (int(str(remaining - 10000).replace("-", "")) / 10000) * 100
            self.widget.subtitle.setText(
                f"Il computer verrà riavviato tra {round(remaining / 1000)} secondi."
            )
            bar.setProperty("value", percent)

        print("HO ROTTO IL SISTEMA")
