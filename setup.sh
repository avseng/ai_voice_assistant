#!/bin/bash

sudo apt-get update
yes | sudo apt-get upgrade

echo "Installing packages ............................................................"
echo "Installing package: python3-pip ......................"
yes | sudo apt-get install python3-pip
echo "Installing package: speechrecognition ......................"
yes | sudo pip3 install speechrecognition
echo "Installing package: weathercom ......................"
yes | sudo pip3 install weathercom
echo "Installing package: portaudio19-dev ......................"
yes | sudo apt-get install portaudio19-dev
echo "Installing package: gTTS ......................"
yes | sudo pip3 install gTTS
echo "Installing package: pyaudio ......................"
yes | sudo pip3 install pyaudio
echo "Installing package: libsdl-ttf2.0-0 ......................"
yes | sudo apt-get install libsdl-ttf2.0-0
echo "Installing package: libsdl-mixer1.2 ......................"
yes | sudo apt-get install libsdl-mixer1.2
echo "Installing package: flac ......................"
yes | sudo apt-get install flac
echo "Installing package: pygame ......................"
yes | sudo pip3 install pygame
echo "Installing package: beautifulsoup4 ......................"
yes | sudo pip3 install beautifulsoup4
echo "Installing package: lxml ......................"
yes | sudo pip3 install lxml
echo "Installing package: googletrans ......................"
yes | sudo pip3 install googletrans
echo "Installing package: wikipedia ......................"
yes | sudo pip3 install wikipedia
echo "Installing package: spidev ......................"
yes | sudo pip3 install spidev


echo "Installing sound card: seeed ....................."
git clone https://github.com/respeaker/seeed-voicecard.git
cd seeed-voicecard
sudo ./install.sh  --compat-kernel
