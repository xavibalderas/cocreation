#!/bin/sh

mkdir /home/pi/Apps
cd Apps
git clone https://github.com/xavibalderas/cocreation.git
cd cocreation
sudo apt install libcups2-dev ttf-mscorefonts-installer
sudo pip install pycups reportlab
echo Installed!


