import openai, os, time
from . import ChatHelper, TranscriptionHelper, TTSHelper

openai.api_key = os.getenv("OPENAI_API_KEY")
tts_endpoint = "http://192.168.1.50:59125/api/tts"
rate_limit_wait = 5

class AIHelper:
    def __init__(self):
        self.ChatHelper = ChatHelper.ChatHelper()
        self.TranscriptionHelper = TranscriptionHelper.TranscriptionHelper()
        self.TTSHelper = TTSHelper.TTSHelper(endpoint=tts_endpoint)

    def openai_wrapper(func):
        def wrap(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except openai.error.RateLimitError:
                end = time.time() + rate_limit_wait
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

    @openai_wrapper
    def transcribe(self, filename:str):
        return self.TranscriptionHelper.transcribe(filename)

    @openai_wrapper
    def text_to_wav(self, *args, **kwargs):
        return self.TTSHelper.text_to_wav(*args, **kwargs)