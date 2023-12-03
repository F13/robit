import abc

import requests


class TranscriptionHelper(abc.ABC):
    @abc.abstractmethod
    def transcribe(self):
        raise NotImplementedError

class Custom_TranscriptionHelper(TranscriptionHelper):
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def transcribe(self, data, args=None):
        try:
            response = requests.post(self.endpoint, data=data, params=args)
        except requests.exceptions.ConnectionError as e:
            raise TranscriptionError(e)
        return response.text
    
class TranscriptionError(Exception):
    pass