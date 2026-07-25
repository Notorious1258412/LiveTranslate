import requests


class OllamaTranslator:

    def __init__(self, model="hy-mt:latest"):

        self.model = model

        print(
            "使用Ollama模型:",
            model
        )


    def translate(self,text):

        if not text:
            return ""


        prompt = f"""
<think>false</think>

Translate the following English into Traditional Chinese.
Only output translation.

{text}
"""


        r=requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model":self.model,
                "prompt":prompt,
                "stream":False,
                "options":{
                    "temperature":0
                }
            }
        )


        result = r.json()["response"]

        if "</think>" in result:
            result = result.split("</think>")[-1]

        return result.strip()