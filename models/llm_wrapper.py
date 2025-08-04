from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

class LLMWrapper:
    def __init__(self, config):
        self.client = OpenAI(api_key=config["api_key"])
        self.model = config.get("model", "gpt-4")

    def generate(self, prompt: str) -> str:
        messages: list[ChatCompletionMessageParam] = [
            {"role": "user", "content": prompt}
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content