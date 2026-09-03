from app.ai.llm.client import OpenAIClient

def test_openai_client_initializes():
    client = OpenAIClient()

    assert client.client is not None