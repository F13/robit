# robit

Proof-of-concept of a conversational robit using GPT, WhisperAI, and Mimic 3. Inspired by https://www.youtube.com/watch?v=bO-DWWFolPw.

## Running

1. Install requirements:
    - `python -m pip install -r requirements.txt`
      - You may have to install some additional libraries depending on your system. For example, in Ubuntu, you may have to run `sudo apt install portaudio19-dev`.
1. Get yourself a running transcription service. I've been using [whisper-jax](https://github.com/sanchit-gandhi/whisper-jax) with good success.
    - You can pass in the endpoint for your transcription service when AIHelper is instantiated (in `robit.py`):
        - `ai = AIHelper.AIHelper(transcription_endpoint="foo")`
1. If you want to use Mimic 3 instead of Open AI for TTS:
    - Spin up Mimic 3, for example using docker:
        https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mimic-tts/mimic-3#docker-image
    - Use `Custom_TTSHelper` instead of `OpenAI_TTSHelper` in `AIHelper`'s `__init__.py`
        - You may want to pass in a different TTS endpoint for Mimic 3 when AIHelper is instantiated (in `robit.py`):
            - `ai = AIHelper.AIHelper(tts_endpoint="foo")`
1. Put your OpenAI API key in the env (or stick it in some other way, I'm not your mom):
    - `export OPENAI_API_KEY=foobar`
1. Run `robit.py`.
    - `python robit.py` (or some other way. I don't know your life. Calm down.)
