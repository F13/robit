import os
import time

import openai

from . import ChatHelper, TranscriptionHelper, TTSHelper

tts_endpoint = os.getenv("ROBIT_TTS_ENDPOINT", "http://localhost:59125/api/tts")
transcription_endpoint = os.getenv("ROBIT_TRANSCRIPTION_ENDPOINT", "http://localhost:4444/transcribe")

class AIHelper:
    def __init__(self, openai_client=None, tts_endpoint=tts_endpoint, transcription_endpoint=transcription_endpoint):
        self.openai_client = openai_client
        if not self.openai_client:
            self.openai_client = openai.OpenAI()
        
        self.ChatHelper = ChatHelper.OpenAI_AssistantHelper(client=self.openai_client)
        self.TranscriptionHelper = TranscriptionHelper.Custom_TranscriptionHelper(endpoint=transcription_endpoint)
        self.TTSHelper = TTSHelper.OpenAI_TTSHelper(client=self.openai_client)
        #self.TTSHelper = TTSHelper.Custom_TTSHelper(endpoint=tts_endpoint)

    def openai_wrapper(func):
        def wrap(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except openai.RateLimitError:
                end = time.time() + 10
                while time.time() < end:
                    print(f"Rate limited ({int(end - time.time()) + 1}) ", end="\r")
                print("\x1b[K", end="")
                return AIHelper.openai_wrapper(func)(*args, **kwargs)
        return wrap

    @openai_wrapper
    def chat(self, message:str):
        return self.ChatHelper.chat(message)
    
    @openai_wrapper
    def create_summary(self):
        return self.ChatHelper.create_summary()

    def transcribe(self, filename:str):
        return self.TranscriptionHelper.transcribe(filename)

    @openai_wrapper
    def text_to_speech(self, *args, **kwargs):
        return self.TTSHelper.text_to_speech(*args, **kwargs)