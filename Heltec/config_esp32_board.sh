#!/bin/bash
usermod -a -G dialout $USER
apt-get install git
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
pip install pyserial
mkdir -p ~/Arduino/hardware/espressif
cd ~/Arduino/hardware/espressif
git clone https://github.com/espressif/arduino-esp32.git esp32
cd esp32
git submodule update --init --recursive
cd tools
python3 get.py
apt install python-serial
apt install unar -y
