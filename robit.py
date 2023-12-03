#!/usr/bin/env python3

import json
import logging
import os
import tempfile
import time

import dotenv

dotenv.load_dotenv()

from helpers import AIHelper, AudioHelper


class Robit():
    def __init__(self):
        

        logging.basicConfig()
        self.logger = logging.getLogger("robit")
        self.logger.setLevel(os.getenv("ROBIT_LOG_LEVEL", "INFO").upper())

        self.ai = AIHelper.AIHelper()

    def start(self):
        #TODO: Background constant listening, with interrupt (separate listen_loop func probably)
        #TODO: Eventually, wake word
        while True:
            try:
                timestats = {}
                start = time.perf_counter()

                tf = tempfile.NamedTemporaryFile(suffix=".wav")
                self.logger.debug("Listening...")
                AudioHelper.AudioHelper(dst_filename=tf.name).get_soundbite()

                self.logger.debug("Transcribing...")
                with open(tf.name, 'rb') as ofile:
                    user_message = self.ai.transcribe(ofile.read())
                    timestats['transcription'] = time.perf_counter() - start
                tf.close()
                self.logger.debug(f"Transcription [{round(timestats['transcription'], 2)}s]: {user_message}")

                self.logger.debug("Thinking...")
                bot_message = self.ai.chat(user_message)
                timestats['chat'] = time.perf_counter() - (start + timestats['transcription'])
                self.logger.debug(f"Response [{round(timestats['chat'], 2)}s]: {bot_message}")

                self.logger.debug("Generating voice...")
                audio = self.ai.text_to_speech(bot_message)
                timestats['tts'] = time.perf_counter() - (start + timestats['chat'] + timestats['transcription'])
                timestats['total'] = time.perf_counter() - start
                self.logger.debug(f"Speaking [{round(timestats['tts'], 2)}s]: [...]")
                AudioHelper.AudioHelper().say(audio, format="mp3")

                self.logger.info(json.dumps({k:round(v, 2) for k,v in timestats.items()}, indent=2))
            except KeyboardInterrupt:
                self.logger.info("Shutting down from console request")
                message_count = len(self.ai.ChatHelper.get_messages())
                if message_count != 0:
                    self.logger.info(f"Generating summary [{message_count} messages]...")
                    self.logger.info(f"Summary: // {self.ai.create_summary()} //")
                quit()
            except AIHelper.TranscriptionHelper.TranscriptionError as e:
                self.logger.error(f"There was an error transcribing: {e}")
            except Exception as e:
                self.logger.critical(f"Unhandled exception! {e}")
            finally:
                tf.close()

if __name__ == "__main__":
    Robit().start()