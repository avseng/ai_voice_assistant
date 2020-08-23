#!/bin/sh
sleep 10
python3 /home/pi/ai_voice_assistant/main.py >> /mnt/ramdisk/voice.txt 2>&1
