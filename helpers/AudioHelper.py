import pyaudio
import math
import struct
import wave
import time
from pydub import AudioSegment
from pydub.playback import play

Threshold = 10

SHORT_NORMALIZE = (1.0/32768.0)
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
swidth = 2

TIMEOUT_LENGTH = .5

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

    def __init__(self, src_filename=None, dst_filename=None):
        self.src_filename=src_filename
        self.dst_filename=dst_filename
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
        self.write(b''.join(rec))

    def write(self, recording):
        with wave.open(self.dst_filename, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(recording)
    
    def listen(self, dst_file=None):
        if dst_file:
            self.dst_filename = dst_file
        while self.rms(self.stream.read(chunk)) <= Threshold:
            pass
        self.record()

    def say(self, audio, format):
        if not audio:
            audio = self.src_file
        if format == "wav":
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
        elif format == "mp3":
            song = AudioSegment.from_mp3(audio)
            play(song)
