#!/usr/bin/env python3
#
# Copyright 2019 Geoff Williams <geoff@declarativesystems.com>
#
# This example script is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version so long as this copyright notice remains intact.
#
# This example script is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this example script.  If not, see <http://www.gnu.org/licenses/>.

__author__ = """Geoff Williams <geoff@declarativesystems.com>"""
__copyright__ = """Copyright 2019 Geoff Williams"""

"""
Allocate free space to a partition. This demo is setup for a raw image file
`sdcard.img` which is assumed to already contain partitions but with some
unallocated space at the end of the drive. If you have an image file that you
have _grown_ for this purpose (eg with `dd` or `truncate`) and it is GPT, you
need to run:

  sgdisk -e FILE

before running this script since GPT demands 33 backup blocks at the end of
the disk. If you forget to do this you will get errors like this:

  File "/home/geoff/.local/lib/python3.7/site-packages/parted/decorators.py", line 42, in new
    ret = fn(*args, **kwds)
  File "/home/geoff/.local/lib/python3.7/site-packages/parted/disk.py", line 245, in addPartition
    constraint.getPedConstraint())
_ped.PartitionException: Unable to satisfy all constraints on the partition.

Lets grow our SD card image:
  $ dd if=/dev/zero bs=1M count=100 >> sdcard.img
  $ sgdisk -e sdcard.img
"""

# pip3 install pyparted
import parted


def partition(device):
    device = parted.getDevice(device)
    disk = parted.newDisk(device)

    # grab the free space region at the end of the disk
    disk.deleteAllPartitions()

    geometry_root = parted.Geometry(device=device, start=2048, end=32901119)
    geometry_extended = parted.Geometry(
        device=device, start=32901120, end=disk.getFreeSpaceRegions()[-1].end
    )
    geometry_swap = parted.Geometry(device=device, start=32903168, end=37029888)
    geometry_var = parted.Geometry(device=device, start=37031936, end=99946495)
    geometry_secours = parted.Geometry(device=device, start=99944448, end=100968447)
    geometry_home = parted.Geometry(
        device=device, start=100972544, end=geometry_extended.end
    )

    # filesystem will be shown as blank by parted until it has been _formatted_
    filesystem_root = parted.FileSystem(type="ext4", geometry=geometry_root)
    filesystem_extended = parted.FileSystem(type="ext4", geometry=geometry_extended)
    filesystem_swap = parted.FileSystem(type="linux-swap(v1)", geometry=geometry_swap)
    filesystem_var = parted.FileSystem(type="ext4", geometry=geometry_var)
    filesystem_secours = parted.FileSystem(type="ext4", geometry=geometry_secours)
    filesystem_home = parted.FileSystem(type="ext4", geometry=geometry_home)

    root = parted.Partition(
        disk=disk,
        type=parted.PARTITION_NORMAL,
        fs=filesystem_root,
        geometry=geometry_root,
    )

    extended = parted.Partition(
        disk=disk,
        type=parted.PARTITION_EXTENDED,
        fs=filesystem_extended,
        geometry=geometry_extended,
    )
    swap = parted.Partition(
        disk=disk,
        type=parted.PARTITION_LOGICAL,
        fs=filesystem_swap,
        geometry=geometry_swap,
    )

    var = parted.Partition(
        disk=disk,
        type=parted.PARTITION_LOGICAL,
        fs=filesystem_var,
        geometry=geometry_var,
    )

    secours = parted.Partition(
        disk=disk,
        type=parted.PARTITION_LOGICAL,
        fs=filesystem_secours,
        geometry=geometry_secours,
    )

    home = parted.Partition(
        disk=disk,
        type=parted.PARTITION_LOGICAL,
        fs=filesystem_home,
        geometry=geometry_home,
    )

    partitions = [root, extended, swap, var, secours, home]

    for part in partitions:
        disk.addPartition(partition=part, constraint=device.minimalAlignedConstraint)
    return disk.commit()
