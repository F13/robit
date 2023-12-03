# robit

Proof-of-concept of a conversational robit using GPT, WhisperAI, and Mimic 3. Inspired by https://www.youtube.com/watch?v=bO-DWWFolPw.

## Running

1. Install requirements:
    - `python -m pip install -r requirements.txt`
      - You may have to install some additional libraries depending on your system. For example, in Ubuntu, you may have to run `sudo apt install portaudio19-dev`.
1. Get yourself a running transcription service. I've been using [whisper-jax](https://github.com/sanchit-gandhi/whisper-jax) with good success.
1. If you want to use Mimic 3 instead of Open AI for TTS:
    - Spin up Mimic 3, for example using docker:
        https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mimic-tts/mimic-3#docker-image
    - Use `Custom_TTSHelper` instead of `OpenAI_TTSHelper` in `AIHelper`'s `__init__.py`.
    - Change the `format` argument in `AudioHelper.say()` to `wav` (Mimic 3 outputs a wav, OpenAI an MP3).
1. Put your settings in the env (or stick them in some other way, I'm not your mom).
    - This project uses `dotenv`, so all you have to do is create a `.env` file in the root of the repo.
    - Supported settings:
        - `OPENAI_API_KEY` - API key for OpenAI. Required (chat responses use GPT, and TTS uses OpenAI's TTS model by default)
        - `ROBIT_TRANSCRIPTION_ENDPOINT` - Endpoint for a transcription service. Defaults to `http://localhost:4444/transcribe`.
        - `ROBIT_TTS_ENDPOINT` - Endpoint for a TTS service. For use with `Custom_TTSHelper`. Defaults to `http://localhost:59125/api/tts` (the default Mimic 3 URL).
        - `ROBIT_LOG_LEVEL` - Specify output log level. Recommend setting this to `DEBUG` especially for now.
1. Run `robit.py`.
    - `python robit.py` (or some other way. I don't know your life. Calm down.)
