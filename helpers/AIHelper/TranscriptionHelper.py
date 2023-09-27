import openai, json

class TranscriptionHelper:
    def transcribe(self, file:str):
        with open(file, "rb") as fopen:
            return openai.Audio.transcribe("whisper-1", fopen, language="en").text

        # return json.loads(transcript)["text"]