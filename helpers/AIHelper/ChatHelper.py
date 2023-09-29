import openai, os, tiktoken

class ChatHelper:
    def __init__(self):
        self.history = []
        self.model = "gpt-3.5-turbo"
        self.max_response_tokens = 15
        
        with open(os.path.join(os.path.dirname(__file__), "config/prompts/system.txt"), "r") as fopen:
            self.system_prompt = fopen.read()

        self.history.append({"role": "system", "content": self.system_prompt})

    def get_user_message(self):
        return "Hello, robit!"

    def get_robit_message(self, messages:list):
        if not messages:
            messages = self.history

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            max_tokens=self.get_total_allowed_response_tokens(messages)
        )
        
        return response.choices[0].message.content
    
    def chat(self, message:str):
        self.history.append({
            "role": "user", "content": message
        })
        response = self.get_robit_message(self.history)
        self.history.append({
            "role": "assistant", "content": response
        })
        return response

    def get_total_allowed_response_tokens(self, messages:dict):
        encoding = tiktoken.encoding_for_model(self.model)
        num_tokens = 0
        for message in messages:
            num_tokens += 3
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += 1
        num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
        return num_tokens + self.max_response_tokens
    
    def create_summary(self):
        summary_prompt = "Please summarize this conversation in three sentences or less.\
                          Be sure to include important personal details or memories we shared.\
                          This summary will be your only memory of our conversation in the future."
        return self.get_robit_message(self.history + [{"role":"user", "content":summary_prompt}])