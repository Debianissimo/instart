import asyncio
import json
import subprocess

app = type("marso", (object,), {"loop": asyncio.get_event_loop()})


async def main():
    disks = [
        a
        for a in (
            await app.loop.run_in_executor(
                None,
                lambda: subprocess.run(
                    "lsblk -b -d -o NAME,SIZE",
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
    print(disks)
    for disk in disks:
        result[disk.split()[0]] = int(disk.split()[1])
    result = json.dumps(result)
    return result


print(app.loop.run_until_complete(main()))
