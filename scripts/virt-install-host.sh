#!/usr/bin/sh
VM_NAME=$1
VM_NETWORK=$2
virt-install \
  --name "${VM_NAME}" \
  --memory 2048 \
  --vcpus 4 \
  --disk size=25,cache=writeback,bus=scsi,pool=<VIRSH_POOL> \
  --pxe \
  --connect qemu:///system \
  --controller scsi,model=virtio-scsi \
  --console pty,target_type=virtio \
  --os-variant centos7.0 \
  --network network="${VM_NETWORK}" \
  --watchdog default \
  --rng /dev/urandom \
  --graphics vnc \
  --debug

