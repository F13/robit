import openai, os

class ChatHelper:
    def __init__(self):
        self.history = []
        
        with open(os.path.join(os.path.dirname(__file__), "config/prompts/system.txt"), "r") as fopen:
            self.system_prompt = fopen.read()

        self.history.append({"role": "system", "content": self.system_prompt})

    def get_user_message(self):
        return "Hello, robit!"

    def get_robit_message(self, messages:list):
        if not messages:
            messages = self.history

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages)
        
        return response.choices[0].message.content
    
    def chat(self, message:str):
        try:
            self.history.append({
                "role": "user", "content": message
            })
            response = self.get_robit_message(self.history)
            self.history.append({
                "role": "assistant", "content": response
            })
            return response
        except Exception as e:
            print(f"panic: {e}")