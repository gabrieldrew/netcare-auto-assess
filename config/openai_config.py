import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

_client = None


def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("Set the OPENAI_API_KEY environment variable.")
        _client = OpenAI(api_key=api_key)
    return _client
