import pyaudio
import wave
import speech_recognition as sr
import time
from gtts import gTTS
from pygame import mixer
import os
#import weathercom
import json
#import numpy as np
import urllib.request



#AUDIO_FILENAME = "/mnt/ramdisk/myspeech.wav"
AUDIO_PLAYBACK_FILENAME = "/mnt/ramdisk/audio_play_back.mp3"


r = sr.Recognizer()


def record_audio(RECORD_SECONDS, WAVE_OUTPUT_FILENAME):
    RESPEAKER_RATE = 44100
    RESPEAKER_CHANNELS = 2
    RESPEAKER_WIDTH = 2
    # run getDeviceInfo.py to get index
    RESPEAKER_INDEX = 3  # refer to input device id
    CHUNK = 380
    #RECORD_SECONDS = 5
    # WAVE_OUTPUT_FILENAME = "/home/pi/ai_voice_assistant/venv/ai_voice_assistance/output.wav"
    p = pyaudio.PyAudio()
    stream = p.open(
        rate=RESPEAKER_RATE,
        format=p.get_format_from_width(RESPEAKER_WIDTH),
        channels=RESPEAKER_CHANNELS,
        input=True,
        input_device_index=RESPEAKER_INDEX)


#    stream = sb_stream
#    stream.start_stream()
    print("* recording")

    frames = []

    for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(RESPEAKER_CHANNELS)
    wf.setsampwidth(p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH)))
    wf.setframerate(RESPEAKER_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def processVoice(audio_file):
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
        s = ''
        try:
            s =r.recognize_google(audio)
        except Exception as e:
            a=1
        return s.lower()



def recognizeSpeech(audio_file, duration):
    record_audio(duration, audio_file)
    s = processVoice(audio_file)
    return s.lower()


def audio_playback(text):
    tts = gTTS(text=text, lang='en-us')
    tts.save(AUDIO_PLAYBACK_FILENAME)
    mixer.init()
    mixer.music.load(AUDIO_PLAYBACK_FILENAME)
    mixer.music.play()
    while mixer.music.get_busy():
        pass
    os.remove(AUDIO_PLAYBACK_FILENAME)



def wake_word_detection(text):
    if "gideon" in text:
        return True
    else:
        return False




def youtubeStatus():
    name = "UC4t2LRjlTnKg_sT4E75QRNA"
    key = "AIzaSyDYnnp1gnefpZ9s2_Mojakuz6eu-3huXH8"
    data = urllib.request.urlopen(
        "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + name + "&key=" + key).read()
    subs = json.loads(data)["items"][0]["statistics"]["subscriberCount"]
    view_count = json.loads(data)["items"][0]["statistics"]["viewCount"]
    total_video = json.loads(data)["items"][0]["statistics"]["videoCount"]

    return subs, view_count, total_video
