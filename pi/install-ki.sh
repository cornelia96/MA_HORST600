#!/bin/sh

#Wird alles als root installiert !!!

#System updaten
#sudo apt-get update
#sudo apt-get upgrade
#sudo apt-get install git

#git clone https://gitlab.com/digitalisierungszentrum/showcase-ki.git

#Software installieren
sudo apt-get -y install python3-dev python3-pip python3-venv python3-picamera git libatlas-base-dev libopenjp2-7-dev
sudo apt-get -y install -y libatlas-base-dev libhdf5-dev libc-ares-dev libeigen3-dev build-essential libsdl-ttf2.0-0 python-pygame festival python3-h5py


#pip updaten
sudo pip3 install --upgrade pip

#Python libraries installieren
sudo pip3 install Pillow numpy pygame RPi.GPIO

#Aktuelles Tensorflow laden (alt)
#mkdir lib
#cd lib
#wget https://raw.githubusercontent.com/PINTO0309/Tensorflow-bin/master/tensorflow-2.3.1-cp37-none-linux_armv7l_download.sh
#chmod a+x ./tensorflow-2.3.1-cp37-none-linux_armv7l_download.sh
#./tensorflow-2.3.1-cp37-none-linux_armv7l_download.sh
#sudo pip3 install --upgrade setuptools
#sudo pip3 install tensorflow-*-linux_armv7l.whl
#
#
#Mit Google Original Sourcen (neu)
#lib von https://storage.googleapis.com/tensorflow/raspberrypi/tensorflow-2.3.0rc2-cp35-none-linux_armv6l.whl
mkdir lib
cd lib
#geht nicht... get https://storage.googleapis.com/tensorflow/raspberrypi/tensorflow-2.3.0rc2-cp35-none-linux_armv6l.whl
#file: https://drive.google.com/file/d/12ZvJmac9P3-_Ha4_Z6ktvI4YOnjIiSKG/view?usp=sharing
#wget 'https://storage.googleapis.com/tensorflow/raspberrypi/tensorflow-2.3.0rc2-cp35-none-linux_armv7l.whl' -O tensorflow-2.3.0rc2-cp35-none-linux_armv7l.whl
#wget https://drive.google.com/file/d/12ZvJmac9P3-_Ha4_Z6ktvI4YOnjIiSKG/view?usp=sharing

curl -sc /tmp/cookie "https://drive.google.com/uc?export=download&id=1o-H38Wpl38Hk3uByNukBWId8VieVwGt0" > /dev/null
CODE="$(awk '/_warning_/ {print $NF}' /tmp/cookie)"
curl -Lb /tmp/cookie "https://drive.google.com/uc?export=download&confirm=${CODE}&id=1o-H38Wpl38Hk3uByNukBWId8VieVwGt0" -o tensorflow-2.3.1-cp37-none-linux_armv7l.whl
echo Download finished.

sudo pip3 install --upgrade setuptools
sudo pip3 install tensorflow-2.3.1-cp37-none-linux_armv7l.whl

cd ..

#Kamera aktivieren ab hier manuelle Interaktion notwendig
#3 - interfaces -> Camera -> Activate 
sudo raspi-config 


