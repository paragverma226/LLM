import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

# Fetch and set OpenAI API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY is not set in the environment.")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


class LanguageModel:
    """
    A wrapper class to initialize and return the specified OpenAI language model.
    """

    def __init__(self, model_name: str = "gpt-4o"):
        if not model_name:
            raise ValueError("A valid model name must be provided.")
        self.model_name = model_name
        self.model = ChatOpenAI(model=self.model_name)

    def get_model(self):
        """
        Returns the initialized OpenAI chat model.
        """
        return self.model


if __name__ == "__main__":
    llm = LanguageModel()
    chat_model = llm.get_model()
    reply = chat_model.invoke("hi")
    print(reply)
