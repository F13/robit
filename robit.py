#!/usr/bin/env python3

from helpers import AIHelper, AudioHelper

chatbot = AIHelper.ChatHelper()

# audio.listen()
# user_message = AIHelper.TranscriptionHelper().transcribe("/tmp/audio/2.wav")

def process_audio(file):
    user_message = AIHelper.TranscriptionHelper().transcribe(file)
    print(user_message)
    bot_message = chatbot.chat(user_message)
    print(bot_message)
    wav = AIHelper.TTSHelper().text_to_wav(bot_message, {"lengthScale":"0.75"})
    AudioHelper.AudioHelper().say(wav)
try:
    if __name__ == "__main__":
        while True:
            process_audio(AudioHelper.AudioHelper().listen())
except KeyboardInterrupt:
    print(f"Full history log: {chatbot.history}")