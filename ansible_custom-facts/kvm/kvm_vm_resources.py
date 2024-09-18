#!/usr/bin/python
import os
import json

def vm_ram():
    """Returns a dictionary of VM domain names and the amount of RAM configured
    for them in kilobytes."""
    myList =  os.popen("""virsh list --all | awk '/running/ { print $2}' | while read i; do printf "${i} "; sudo virsh dumpxml "${i}" | grep 'memory ' | egrep -o '[0-9]*';done""").read().strip().split('\n')
    myDict = {}
    for item in myList:
        if item:
          split_item = item.split()
          myDict[split_item[0]] = int(split_item[1])
    return(myDict)

def vm_cpu():
    """Returns a dictionary of VM domain names and the number of VCPUs configured
     for them."""
    myList = os.popen(r"""virsh list --all | awk '/running/ { print $2}' | while read i; do printf "${i} "; sudo virsh dumpxml "${i}" | grep 'vcpu ' | egrep -o '[0-9]*';done""").read().strip().split('\n')
    myDict =  {}
    for item in myList:
        if item:
          split_item = item.split()
          myDict[split_item[0]] = int(split_item[1])
    return(myDict)

def node_ram():
    """Returns the total amount of RAM on the node in kilobytes."""
    totalRamKb = int(os.popen(r"""free -k | awk '/Mem/ { print $2}'""").read().strip())
    return(totalRamKb)

def node_cpu():
    """Returns the number of CPUs from 'lscpu'"""
    totalCpus = int(os.popen(r"""lscpu | grep -v 'NUMA' | awk '/CPU\(s\):/ { print $2}'""").read().strip())
    return(totalCpus)

if __name__ == "__main__":
    vm_ram_total = 0
    node_ram_total_gb = (node_ram() / 1000 / 1000)
    node_cpu_total = node_cpu()
    for value in vm_ram().values():
        vm_ram_total += value
    vm_ram_total_gb = (vm_ram_total / 1000 / 1000)
    percentage_total = (float(vm_ram_total_gb) / float(node_ram_total_gb) * 100)
    vm_cpu_total = 0
    for value in vm_cpu().values():
        vm_cpu_total += value
    print('Total RAM assigned for VMs:           ' + str(vm_ram_total_gb) + ' GB')
    print('Total RAM available on node:          ' + str(node_ram_total_gb) + ' GB')
    print('Percentage RAM configured for VMs:    '  + str(round(percentage_total,1)) + '%')
    print('')
    print('Total CPUs on node:                   ' + str(node_cpu_total))
    print('Total VCPUs assigned to VMS:          ' + str(vm_cpu_total))
    print('')
