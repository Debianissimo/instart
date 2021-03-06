#!/usr/bin/env python3

import parted
import os

efi = os.path.exists("/sys/firmware/efi")
ty = "gpt" if efi else "msdos"


def partition(device):
    device = parted.getDevice(device)
    disk = parted.freshDisk(device, ty)

    disk.deleteAllPartitions()

    partition_type = parted.PARTITION_NORMAL if efi else parted.PARTITION_LOGICAL
    home_end = disk.getFreeSpaceRegions()[-1].end - 1000000
    geometry_extended = disk.getFreeSpaceRegions()[-1]
    filesystem_extended = None
    extended = None
    geometry_efi = None
    filesystem_efi = None
    esp = None

    geometry_root = parted.Geometry(device=device, start=2048, end=32901119)
    if not efi:
        geometry_extended = parted.Geometry(
            device=device, start=32901120, end=disk.getFreeSpaceRegions()[-1].end
        )
        home_end = geometry_extended.end
    geometry_swap = parted.Geometry(device=device, start=32903168, end=37029888)
    geometry_var = parted.Geometry(device=device, start=37031936, end=99946495)
    geometry_secours = parted.Geometry(device=device, start=99944448, end=102041599)
    geometry_home = parted.Geometry(
        device=device, start=102043648, end=home_end
    )
    if efi:
        geometry_efi = parted.Geometry(
            device=device, start=home_end + 1, end=disk.getFreeSpaceRegions()[-1].end
        )

    filesystem_root = parted.FileSystem(type="ext4", geometry=geometry_root)
    if not efi:
        filesystem_extended = parted.FileSystem(type="ext4", geometry=geometry_extended)

    filesystem_swap = parted.FileSystem(type="linux-swap(v1)", geometry=geometry_swap)
    filesystem_var = parted.FileSystem(type="ext4", geometry=geometry_var)
    filesystem_secours = parted.FileSystem(type="ext4", geometry=geometry_secours)
    filesystem_home = parted.FileSystem(type="ext4", geometry=geometry_home)
    if efi:
        filesystem_efi = parted.FileSystem(type="fat32", geometry=geometry_efi)

    root = parted.Partition(
        disk=disk,
        type=parted.PARTITION_NORMAL,
        fs=filesystem_root,
        geometry=geometry_root,
    )

    if not efi:
        extended = parted.Partition(
            disk=disk,
            type=parted.PARTITION_EXTENDED,
            fs=filesystem_extended,
            geometry=geometry_extended,
        )

    swap = parted.Partition(
        disk=disk,
        type=partition_type,
        fs=filesystem_swap,
        geometry=geometry_swap,
    )

    var = parted.Partition(
        disk=disk,
        type=partition_type,
        fs=filesystem_var,
        geometry=geometry_var,
    )

    secours = parted.Partition(
        disk=disk,
        type=partition_type,
        fs=filesystem_secours,
        geometry=geometry_secours,
    )

    home = parted.Partition(
        disk=disk,
        type=partition_type,
        fs=filesystem_home,
        geometry=geometry_home,
    )
    if efi:
        esp = parted.Partition(
            disk=disk,
            type=partition_type,
            fs=filesystem_efi,
            geometry=geometry_efi
        )

    partitions = [root, extended, swap, var, secours, home, esp]

    for part in partitions:
        if not part:
            continue

        disk.addPartition(partition=part, constraint=device.minimalAlignedConstraint)

    cmt = disk.commit()
    if efi:
        esp.setFlag(18)
        return disk.commit()

    return cmt
