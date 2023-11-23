#!/usr/bin/env python3

from helpers import AIHelper, AudioHelper
import tempfile, os, time, json

ai = AIHelper.AIHelper()

def process_audio(file):
    timestats = {}
    start = time.perf_counter()
    with open(file, 'rb') as ofile:
        user_message = ai.transcribe(ofile.read())
        timestats['transcription'] = time.perf_counter() - start
    print(user_message)
    bot_message = ai.chat(user_message)
    timestats['chat'] = time.perf_counter() - (start + timestats['transcription'])
    print(bot_message)
    audio = ai.text_to_speech(bot_message)
    timestats['tts'] = time.perf_counter() - (start + timestats['chat'] + timestats['transcription'])
    timestats['total'] = time.perf_counter() - start
    return audio, timestats

if __name__ == "__main__":
    while True:
        try:
            tf = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            print("Listening...")
            AudioHelper.AudioHelper(dst_filename=tf.name).listen()
            audio, timestats = process_audio(tf.name)
            tf.close()

            print(json.dumps(timestats, indent=2))

            AudioHelper.AudioHelper().say(audio, format="mp3")

        except KeyboardInterrupt:
            print("\nGenerating summary...")
            print(f"\nSummary:\n{ai.create_summary()}")
            quit()
        finally:
            os.remove(tf.name)