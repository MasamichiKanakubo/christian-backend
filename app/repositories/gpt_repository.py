from openai import OpenAI
from typing import Dict
import json


class OpenAIRepository:
    def __init__(self, client: OpenAI):
        self.client = client

    def generate_gpt_answer(self, prompt: str) -> Dict[str, str]:
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=messages
        )
        answer = json.loads(completion.choices[0].message.content)
        return answer