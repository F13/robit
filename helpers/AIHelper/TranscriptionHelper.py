import openai, json

class TranscriptionHelper:
    def transcribe(self, file):
        return openai.Audio.transcribe("whisper-1", file, language="en").text