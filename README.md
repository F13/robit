# robit

Proof-of-concept of a conversational robit using GPT, WhisperAI, and Mimic 3. Inspired by https://www.youtube.com/watch?v=bO-DWWFolPw.

## Running

1. Spin up Mimic 3, for example using docker:
    https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mimic-tts/mimic-3#docker-image
2. Install requirements:
  - `python -m pip install -r requirements.txt`
    - You may have to install some additional libraries depending on your system. For example, in Ubuntu, you may have to run `sudo apt install portaudio19-dev`.
3. Put your OpenAI API key in the env (or stick it in some other way, I'm not your mom):
  - `export OPENAI_API_KEY=foobar`
3. Run `robit.py`.
  - `python robit.py` (or some other way. I don't know your life. Calm down.)
    - You may want to pass in a different TTS endpoint for Mimic 3 when AIHelper is instantiated:
      - `ai = AIHelper.AIHelper(tts_endpoint="foo")`