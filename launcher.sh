#!/bin/sh
sleep 3
sudo alsactl restore -f /etc/asound.state
sleep 10
python3 /home/pi/ai_voice_assistant/main.py > /mnt/ramdisk/voice.txt 2>&1

