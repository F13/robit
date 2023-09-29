import pyaudio
import math
import struct
import wave
import time
import os
import tempfile

Threshold = 10

SHORT_NORMALIZE = (1.0/32768.0)
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
swidth = 2

TIMEOUT_LENGTH = .8

class AudioHelper:

    @staticmethod
    def rms(frame):
        count = len(frame) / swidth
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=chunk)
        
    def record(self):
        print('Noise detected, recording beginning')
        rec = []
        current = time.time()
        end = time.time() + TIMEOUT_LENGTH

        while current <= end:
            data = self.stream.read(chunk)

            if self.rms(data) >= Threshold:
                end = time.time() + TIMEOUT_LENGTH

            current = time.time()
            rec.append(data)
        return self.write(b''.join(rec))

    def write(self, recording, filename=None):
        if filename:
            file = os.path.abspath(file)
        else:
            file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")

        with wave.open(file, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(recording)

        return file
    
    def listen(self):
        while self.rms(self.stream.read(chunk)) <= Threshold:
            pass
        return self.record()

    def say(self, audio):
        with wave.open(audio) as wav:
            stream = self.p.open(format = self.p.get_format_from_width(wav.getsampwidth()),
                            channels = wav.getnchannels(),
                            rate = wav.getframerate(),
                            output = True)

            data = wav.readframes(chunk)

            while data:
                stream.write(data)
                data = wav.readframes(chunk)

        stream.stop_stream()
        stream.close()
