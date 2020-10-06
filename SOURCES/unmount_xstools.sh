#!/bin/sh

IFS=,

# Check to ensure tools isos are not mounted

for SRID in $(xe sr-list is-tools-sr="true" params=uuid --minimal); do
    for VDIID in $(xe vdi-list sr-uuid=${SRID} params=uuid --minimal); do
        for VMID in $(xe vbd-list vdi-uuid=${VDIID} params=vm-uuid --minimal); do
            xe vm-cd-eject vm=${VMID}
            if [ $(xe vm-list uuid=${VMID} params=power-state --minimal) != 'halted' ]; then
                echo "Xen tools ISO ejected from running VM (${VMID})"
            fi
        done
    done
done
