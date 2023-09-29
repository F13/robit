#!/usr/bin/env python3

from helpers import AIHelper, AudioHelper
import tempfile, os

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

if __name__ == "__main__":
    while True:
        try:
            tf = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            AudioHelper.AudioHelper(dst_filename=tf.name).listen()
            process_audio(tf.name)
            tf.close()
        except KeyboardInterrupt:
            print("\nGenerating summary...")
            print(f"\nSummary:\n{chatbot.create_summary()}")
            quit()
        finally:
            os.remove(tf.name)