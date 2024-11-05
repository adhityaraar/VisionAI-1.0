#!/usr/bin/env bash

set -e

echo "\n\tBy default, install python3.8.18, if you want another version, follow the manual step mentionned in the README file\n"

sudo apt update
sudo apt-get install python-pip python3-pip -y

echo "\n\tTest installation\n"

python2 -m pip --version
python3 -m pip --version

echo -e "\n\tUpgrading pip\n"

sudo -H python -m pip install --upgrade pip
sudo -H python3 -m pip install --upgrade pip

echo -e "\n\tInstalling dependencies\n"

sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev -y

cd $HOME


echo -e "\n\tDownloading Python3.8.18\n"
wget https://www.python.org/ftp/python/3.8.18/Python-3.8.18.tgz

echo -e "\n\tExtract tar\n"
tar -xf Python-3.8.18.tgz

cd Python-3.8.18

echo -e "\n\tConfigure Python\n"
./configure --enable-optimizations

echo -e "\n\tRun make with all cores\n"
make -j $(nproc)

echo -e "\n\tInstall Python\n"
sudo -H make altinstall

echo -e "\n\tCheck that Python is installed\n"
python3.8 -c 'import sys; print(sys.version)'

echo -e "\n\t Clean up installation\n"
cd $HOME
sudo rm -r Python-3.8.18 && rm Python-3.8.18.tgz

echo -e "\n\tPointing python3 to python version you installed using update-alternatives"
echo -e "\n\tPlease type your current Python version: 3.6, 3.7 ...\n"

read -p "python" version

sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python${version} 0
sudo update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.8 1

echo -e "\n\tConfigure (select the one you want to have priority, make it auto)\n"
sudo update-alternatives --config python3

pip install Flask

echo -e "\n\tDone !\n"
python3 --version

