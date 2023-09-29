#!/usr/bin/env python3

from helpers import AIHelper, AudioHelper
from concurrent.futures import ThreadPoolExecutor

chatbot = AIHelper.ChatHelper()
tts = AIHelper.TTSHelper()
audio = AudioHelper.AudioHelper()

# audio.listen()
# user_message = AIHelper.TranscriptionHelper().transcribe("/tmp/audio/2.wav")

def process_audio(future):
    user_message = AIHelper.TranscriptionHelper().transcribe(future.result())
    print(user_message)
    bot_message = chatbot.chat(user_message)
    print(bot_message)
    wav = tts.text_to_wav(bot_message, {"lengthScale":"0.75"})
    AudioHelper.AudioHelper().say(wav)

executor = ThreadPoolExecutor(max_workers=1)
audio.listen(executor, process_audio)