def prompt(
        self, user_msg=None, prompt=None, stream=False, max_tokens=None, log=None
    ):
    pass

import os
import sys
import requests
import json



class LLM:
    """a basic object to be able to chat with openai using micropython"""

    def __init__(self):
        self.model: str = "gpt-3.5-turbo"
        self.key: str = os.environ["OPENAI_API_KEY"]
        self.max_tokens = 4000  # gpt 3.5 max token is 4,097

        self.chat_endpoint = "https://api.openai.com/v1/chat/completions"

        self.system = """You are a helpful and somewhat humourous assistant who answers concisefully and truthfully. 
        You are talking to a 10 year old kid. Keep the answers short and snappy."""
        self.default_msg = (
            "Who is talking back to me? I need a name and place. Are you online?"
        )

        self.assistant = None
        self.user = None

        self.headers = headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.key}",
        }

    def prompt(self, user_msg=None, prompt=None, stream=False, max_tokens=None):
        """takes in a user msg and replies"""

        messages = [
            {"role": "system", "content": prompt or self.system},
            {"role": "user", "content": user_msg or self.default_msg},
        ]

        payload = {
            "model": self.model,
            "stream": stream,
            "messages": messages,
            "max_tokens": max_tokens or self.max_tokens,
        }

        response = requests.post(self.chat_endpoint, headers=self.headers, json=payload)
        print(response)
        if stream == False:
            reply = response.json()["choices"][0]["message"]["content"]
            return reply
        else:
            return self.stream2(response)
            # return self.stream_reply(payload)

    def stream_reply(self, payload):
        print("Streaming the reply....")
        response = requests.post(self.chat_endpoint, headers=self.headers, json=payload)
        for line in response.iter_lines():
            if line:
                line = line[6:].decode("utf-8")
                if line != "[DONE]":
                    content = json.loads(line)

                    if content["choices"][0]["finish_reason"] != "stop":
                        delta = content["choices"][0]["delta"]["content"]
                        if delta is not None:
                            # print(delta, end="")
                            yield delta

    def stream2(self, response):
        for line in response.iter_lines():
            if line:
                line = line[6:].decode("utf-8")
                if line != "[DONE]":
                    content = json.loads(line)

                    if content["choices"][0]["finish_reason"] != "stop":
                        delta = content["choices"][0]["delta"]["content"]
                        # print(delta, end="")
                        yield delta


model = LLM()

prompt = "you are mark twain"
user_msg = "write a 50 - 80 word story. I am testing the streaming feature."

messages = [
    {"role": "system", "content": prompt},
    {"role": "user", "content": user_msg},
]

payload = {
    "model": "gpt-3.5-turbo",
    "stream": True,
    "messages": messages,
    "max_tokens": 2000,
}

stream = False
reply = model.prompt(payload, stream=stream)

if stream == True:
    text = ""
    for c in reply:
        print(c, end="")
        text += c
else:
    print(reply)

print(f"\n\n\n the final output: \n {text}")


key: str = os.environ["OPENAI_API_KEY"]
chat_endpoint = "https://api.openai.com/v1/chat/completions"

headers = headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {key}",
}


# response = requests.post(chat_endpoint, headers=headers, json=payload, stream=True)
# for line in response.iter_lines(chunk_size=1024):
#     # print(line)
#     if line:
#         line = line[6:].decode("utf-8")
#         if line != "[DONE]":
#             content = json.loads(line)

#             if content["choices"][0]["finish_reason"] != "stop":
#                 delta = content["choices"][0]["delta"]["content"]
#                 if delta is not None:
#                     print(delta, end="")
#                     # yield delta
