#!/usr/bin/env bash

set -e

cd ~
cd Downloads/
git clone https://github.com/Pyrestone/jetson-fan-ctl
cd jetson-fan-ctl
./install.sh

echo -e "\n\tInstall dphys-swapfile\n"
sudo apt-get install dphys-swapfile -y

sed -i 's/CONF_MAXSWAP=2048/CONF_MAXSWAP=6000/g' /sbin/dphys-swapfile
sed -i 's/#CONF_SWAPSIZE=/CONF_SWAPSIZE=6000/g' /etc/dphys-swapfile

echo -e "\n\tDone. The device will reboot to reconfigure swap size\n"

sudo -H pip install -U jetson-stats
sudo reboot
