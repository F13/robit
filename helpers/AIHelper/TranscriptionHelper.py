import openai, os

class TranscriptionHelper:
    def transcribe(self, file):
        try:
            with open(file.name, "rb") as fopen:
                text_result = openai.Audio.transcribe("whisper-1", fopen, language="en").text
        finally:
            os.remove(file.name)
        return text_result