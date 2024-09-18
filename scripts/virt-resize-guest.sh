#!/bin/bash
OLD_DISK_FILE=$1
# Disk size var assumes GBs
NEW_DISK_SIZE=$2

# This is a big one-liner. Make a temp file, format as a disk, 
# then resize the original disk into it and expand the LVM and
# filesystem. I've never had an issue with this, but if the VM
# is important you should test it before running the 'mv` below.

tmp_qcow=$(mktemp) && \
  qemu-img create -f qcow2 \
    -o preallocation=metadata "\
    ${tmp_qcow}" "${NEW_DISK_SIZE}"G && \
  virt-resize --expand /dev/sda2 \
  --LV-expand <PATH_TO_LV> "${OLD_DISK_FILE}" "${tmp_qcow}" && \
  mv "${tmp_qcow}" "${OLD_DISK_FILE}"
