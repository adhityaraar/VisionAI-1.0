#!/usr/bin/env bash

set -e

cd ~/opencv
cd build

echo -e "\n\tRun make with all cores\n"
make -j $(nproc)

echo -e "\n\tRemove the old packages\n"
sudo rm -r /usr/include/opencv4/opencv2

echo -e "\n\tInstall\n"
sudo -H make install
sudo ldconfig

echo -e "\n\tTest installation\n"
python3 -c 'import cv2 as cv; print("openCV version:",cv.__version__,"CudaEnabledDeviceCount",cv.cuda.getCudaEnabledDeviceCount())'

echo -e "\n\tCleaning\n"
make clean
sudo apt-get update
cd $HOME
sudo rm -rf opencv
sudo rm -rf opencv_contrib


echo -e "\n\tDone !\n"
echo "Note: if your going to be building other stuff like Torch or TorchVision leave the swap, your going to need it."
echo "If you don't want, run the following commands:"
echo -e "\t$ sudo /etc/init.d/dphys-swapfile stop"
echo -e "\t$ sudo apt-get remove --purge dphys-swapfile"

echo -e "\n\tBuild pytorch module !\n"
cd ~
cd Downloads
echo -e "git clone --recursive --branch release/1.8 http://github.com/pytorch/pytorch"
cd pytorch
python3 -m pip install -r requirements.txt
python3 setup.py install

echo -e "\n\tBuild vision module !\n"
cd ~
cd Downloads
echo -e "git clone --recursive --branch release/0.9 https://github.com/pytorch/vision.git"
echo -e "git clone https://github.com/pytorch/vision.git"
echo -e "cd vision"
echo -e "git init && git checkout release/0.9"
cd vision
python3 setup.py install


