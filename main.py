import pyaudio
import speech_recognition as sr
import time
import os
import wave
import response
from gtts import gTTS
from pygame import mixer
import valib
from pixels import Pixels



r = sr.Recognizer()

RESPEAKER_RATE = 44100
RESPEAKER_CHANNELS = 2
RESPEAKER_WIDTH = 2
RESPEAKER_INDEX = 0  # refer to input device id
CHUNK = 1024
RECORD_SECONDS_BAK= 5
WAVE_OUTPUT_FILENAME = "/mnt/ramdisk/output.wav"
AUDIO_PLAYBACK_FILENAME = "/mnt/ramdisk/audio_play_back.mp3"



class voice:
    START_RECORDING = True
    def __init__(self):
        START_RECORDING = True
        self.WAVE_OUTPUT_FILENAME = "/mnt/ramdisk/output.wav"
        pyaudio.paInputUnderflow = 1
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            rate=RESPEAKER_RATE,
            format=self.p.get_format_from_width(RESPEAKER_WIDTH),
            channels=RESPEAKER_CHANNELS,
            input=True)

    def voice_command_processor(self):
        with sr.AudioFile(self.WAVE_OUTPUT_FILENAME) as source:
            wait_time = 3
            while True:
                audio = r.record(source, duration=5)
                if audio:
                    break
                time.sleep(1)
                wait_time = wait_time - 1
                if wait_time == 0:
                    break
            text = ''
            try:
                text = r.recognize_google(audio)
                print("you said :: " + text)

            except sr.UnknownValueError as e:
                pass
            except sr.RequestError as e:
                print("service is down")
                pass
            return text.lower()

    def process(self, RECORD_SECONDS):
        print("START_RECORDING :: "+str(a.START_RECORDING))
        if a.START_RECORDING:
            px.wakeup()
            self.stream.start_stream()
            frames = []
            for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
                data = self.stream.read(CHUNK)
                frames.append(data)

            self.stream.stop_stream()
            #stream.close()

            wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(RESPEAKER_CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(self.p.get_format_from_width(RESPEAKER_WIDTH)))
            wf.setframerate(RESPEAKER_RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            px.off()



px = Pixels()
px.wakeup()
time.sleep(1)
px.think()
time.sleep(2)
px.off()
time.sleep(1)

a = voice()

while True:
    a.process(3)
    text = a.voice_command_processor()
    #os.remove(WAVE_OUTPUT_FILENAME)
    if 'pixel' in text or 'Pixel' in text:
        px.wakeup()
        px.think()
        valib.audio_playback('how can i help you')
        time.sleep(0.5)
        a.process(5)
        command = a.voice_command_processor()
        os.remove(WAVE_OUTPUT_FILENAME)
        a.START_RECORDING = False
        px.think()
        status = response.process_text(command, a)
        if 'done' in status:
            a.START_RECORDING = True
    time.sleep(0.5)
    px.off()
    time.sleep(0.5)
