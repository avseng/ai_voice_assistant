*****************************************************************************************************
1. Creating a RAM Disk in raspberry pi. This will help to increase the longsivity of micro sd card.
   we will use this ramdisk to store temp files created by the voice assistant. This file will be
   rempved after reboot.
*****************************************************************************************************
    a. sudo mkdir -p /mnt/ramdisk
    b. sudo chown -R pi:pi /mnt/ramdisk
    c. sudo mount -osize=200M -t tmpfs tmpfs /mnt/ramdisk
    d. sudo nano /etc/fstab
    e. tmpfs /mnt/ramdisk tmpfs defaults,noatime,mode=755,uid=pi,gid=pi,size=200m 0 0
    f. sudo mount -a
    g. df -h
    
*****************************************************************************************************    
2. Install git 
*****************************************************************************************************
    sudo apt-get install git
    
    
*****************************************************************************************************
3. Clone the git repository
*****************************************************************************************************
    git clone https://github.com/avseng/ai_voice_assistant.git
    
*****************************************************************************************************    
4. Run setup.sh to install all the pre-requisite packages and RE-SPEAKER sound card.
*****************************************************************************************************
    cd ai_voice_assistant/
    sudo chmod u+x setup.sh 
    sudo bash setup.sh
    
*****************************************************************************************************
5. check the sound card
*****************************************************************************************************
a. Run below command to get the attached microphone details.

        arecord -l
          **** List of CAPTURE Hardware Devices ****
          card 1: seeed2micvoicec [seeed-2mic-voicecard], device 0: bcm2835-i2s-wm8960-hifi wm8960-hifi-0 [bcm2835-i2s-wm8960-hifi wm8960-hifi-0]
           Subdevices: 0/1
           Subdevice #0: subdevice #0

b. Run below command to get attached speaker details.
  
        aplay -l
          **** List of PLAYBACK Hardware Devices ****
          card 0: ALSA [bcm2835 ALSA], device 0: bcm2835 ALSA [bcm2835 ALSA]
           Subdevices: 6/7
           Subdevice #0: subdevice #0
           Subdevice #1: subdevice #1
           Subdevice #2: subdevice #2
           Subdevice #3: subdevice #3
           Subdevice #4: subdevice #4
           Subdevice #5: subdevice #5
           Subdevice #6: subdevice #6
          card 0: ALSA [bcm2835 ALSA], device 1: bcm2835 IEC958/HDMI [bcm2835 IEC958/HDMI]
           Subdevices: 1/1
           Subdevice #0: subdevice #0
          card 0: ALSA [bcm2835 ALSA], device 2: bcm2835 IEC958/HDMI1 [bcm2835 IEC958/HDMI1]
           Subdevices: 1/1
           Subdevice #0: subdevice #0
          card 1: seeed2micvoicec [seeed-2mic-voicecard], device 0: bcm2835-i2s-wm8960-hifi wm8960-hifi-0 [bcm2835-i2s-wm8960-hifi wm8960-hifi-0]
           Subdevices: 1/1
           Subdevice #0: subdevice #0
         
c. Create a file on /home/pi directory (setting up the record and playback device as default PCM device).
      
          sudo nano .asoundrc
          
e. Add below lines to the file and save it.

          pcm.!default {
           type asym
           capture.pcm "mic"
           playback.pcm "speaker"
          }
          pcm.mic {
           type plug
           slave {
          pcm "hw: 1, 0"
           }
          }
          pcm.speaker {
           type plug
           slave {
          pcm "hw: 0, 0"
           }
          }
          
f. use alsamixer command to control mic sensitivity and speaker vloume.
     
          alsamixer
          
g. Run below command to record your voice 
    
          arecord --format=S16_LE --duration=5 --rate=16000 --file-type=raw out.raw (record your voice).
          
h. Run below command to playback voice and check whether you are able to listen or not
     
          aplay --format=S16_LE --rate=16000 out.raw
          
i. store the alsamixer setting to /etc/asound.state file with below command
          
          sudo alsactl store -f /etc/asound.state (file name must be the same as it is mentioned.)
          


*****************************************************************************************************
6. Update the microphone index number to main.py
*****************************************************************************************************          
    cd ai_voice_assistant/
    python3 check_device_id.py
    
Note down the input device index number from your sound card. This code can be used to check any 
input device index number.

    sudo nano main.py
    
Update the RESPEAKER_INDEX value with exact input device index number.

*****************************************************************************************************
7. Add launcher.sh file to crontab
*****************************************************************************************************
type below command

      contab -e
add below line to at the end of the file and save.

      @reboot nohup bash /home/pi/ai_voice_assistant/launcher.sh &
      
*****************************************************************************************************
8. Update the microphone index number to main.py
*****************************************************************************************************
Reboot the raspberry pi.
