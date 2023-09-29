import openai, os

class TranscriptionHelper:
    def transcribe(self, filename):
        with open(filename, "rb") as fopen:
            text_result = openai.Audio.transcribe("whisper-1", fopen, language="en").text
        return text_result