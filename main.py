from agent.core import AIAgent

if __name__ == "__main__":
    agent = AIAgent()
    response = agent.run("Translate this sentence to Hindi: How are you?")
    print(response)