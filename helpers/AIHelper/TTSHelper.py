import requests, io

class TTSHelper:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def text_to_wav(self, message:str, args:dict=None):
        if not message or len(message) == 0:
            return

        response = requests.post(self.endpoint, data=message, params=args)
        return io.BytesIO(response.content)