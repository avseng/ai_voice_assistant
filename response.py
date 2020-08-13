import valib as va
import weathercom
import action as a
import time
import os


COMMAND_AUDIO_FILE="/mnt/ramdisk/command.wav"

def process_text(text, pa):
    global time

    if "who are you" in text:
        va.audio_playback("i am a i voice assistant system, created by mr. avijit sengupta")


    if "today's weather" in text: 
        va.audio_playback("which city") 
        #time.sleep(0.5) 
        #city = va.recognizeSpeech(COMMAND_AUDIO_FILE, 4) 
        pa.START_RECORDING = True
        pa.process(3)
        city = pa.voice_command_processor()
        print("City :: "+city)
        try: 
            humidity, temp, phrase = a.weatherReport(city) 
            va.audio_playback("currently in " + city + " temperature is " + str(temp) + " degree celsius, " + "humidity is " + str(humidity) + " percent and sky is " + phrase) 
            print("currently in " + city + " temperature is " + str(temp) + "degree celsius, " + "humidity is " + str(humidity) + " percent and sky is " + phrase) 
        except KeyError as e:
            va.audio_playback("sorry, i couldn't get the location")
        #os.remove(COMMAND_AUDIO_FILE)


    if "search" in text :
        va.audio_playback("tell me what to search")
        pa.START_RECORDING = True
        pa.process(5)
        search_data=pa.voice_command_processor()
        #search_data = va.recognizeSpeech(COMMAND_AUDIO_FILE, 4)
        try:
            result = a.google_search(search_data)
            if result:
                va.audio_playback(result)
            else:
                va.audio_playback("sorry, i couldn't find any result for "+search_data)
        except KeyError as e:
            va.audio_playback("sorry, i couldn't find any result for "+search_data)
            pass
        #os.remove(COMMAND_AUDIO_FILE)
    


    if "time" in text:
        current_time = a.current_datetime("time")
        va.audio_playback("right now it is "+current_time)


    if "date" in text:
        date = a.current_datetime("date")
        va.audio_playback("today it is "+date)


    if "reboot" in text:
        va.audio_playback("ok.. rebooting the server")
        a.reboot_server()


    return "done"
