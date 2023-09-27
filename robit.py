#!/usr/bin/env python3

from helpers import AIHelper, AudioHelper

chatbot = AIHelper.ChatHelper()
audio = AudioHelper.AudioHelper()
exit_conditions = (":q", "quit", "exit")

# while True:
#     query = input("> ")
#     if query in exit_conditions:
#         break
#     else:
#         print(chatbot.chat(query))

user_message = AIHelper.TranscriptionHelper().transcribe("/tmp/audio/2.wav")

print(user_message)

bot_message = chatbot.chat(user_message)

print(bot_message)
audio.say(bot_message)

# AudioHelper.AudioHelper().listen()