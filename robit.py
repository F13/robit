#!/usr/bin/env python3

from helpers import AIHelper, AudioHelper
import tempfile, os

ai = AIHelper.AIHelper(tts_endpoint="http://192.168.1.50:59125/api/tts")

def process_audio(file):
    print("Transcription beginning...")
    user_message = ai.transcribe(file)
    print(user_message)
    print("Thinking...")
    bot_message = ai.chat(user_message)
    print(bot_message)
    print("Audioifying...")
    wav = ai.text_to_wav(bot_message, {"lengthScale":"0.75"})
    AudioHelper.AudioHelper().say(wav)

if __name__ == "__main__":
    while True:
        try:
            tf = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            print("Listening...")
            AudioHelper.AudioHelper(dst_filename=tf.name).listen()
            process_audio(tf.name)
            tf.close()
        except KeyboardInterrupt:
            print("\nGenerating summary...")
            print(f"\nSummary:\n{ai.create_summary()}")
            quit()
        finally:
            os.remove(tf.name)