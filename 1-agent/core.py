from models.llm_wrapper import LLMWrapper
from config.config_loader import get_config

class AIAgent:
    def __init__(self):
        config = get_config()
        self.llm = LLMWrapper(config["llm"])

    def run(self, prompt: str) -> str:
        return self.llm.generate(prompt)