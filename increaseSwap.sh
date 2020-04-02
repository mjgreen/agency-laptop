#!/usr/bin/env bash
sudo swapoff /swapfile
sudo fallocate -l 20G /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
sudo swapon -s

# or on zfs

su

zfs create -V 20G -b $(getconf PAGESIZE) -o compression=zle -o logbias=throughput -o sync=always -o primarycache=metadata -o secondarycache=none -o com.sun:auto-snapshot=false rpool/swap
mkswap -f /dev/zvol/rpool/swap
echo /dev/zvol/rpool/swap none swap defaults 0 0 >> /etc/fstab
swapon -av
# reboot to make it take effect