import asyncio
import json
import os
import subprocess
from .partitioning import partition
from PySide2.QtWidgets import QProgressBar, QLabel, QWidget
from PySide2.QtCore import QTimer


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
            if (
                #percent >= 10.025316455696203
                #or line
                #== self._expected_debootstrap_output[-1].replace("I:", "", 1).strip()
                running.returncode
            ):  # cifra completa: 10.025316455696203
                if running.returncode != 0:
                    self.text.setText("C'è stato un errore. Per riprovare, riavvia il PC.")
                    return
                break

        code = 0
        # for code in [
        if not os.path.ismount("/target/proc"):
            code += await self.loop.run_in_executor(
                None,
                lambda: os.system(f"sudo mount -t proc /proc /target/proc"),
            )

        if not os.path.ismount("/target/dev"):
            code += await self.loop.run_in_executor(
                None,
                lambda: os.system(f"sudo mount --rbind /dev /target/dev"),
            ),

        if not os.path.ismount("/target/sys"):
            code += await self.loop.run_in_executor(
                None,
                lambda: os.system(f"sudo mount --rbind /sys /target/sys"),
            ),
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
