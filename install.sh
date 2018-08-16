#!/bin/sh

mkdir /home/pi/Apps
cd Apps
git clone https://github.com/xavibalderas/cocreation.git
cd cocreation
sudo pip install Flask, cups, picamera, reportlab


