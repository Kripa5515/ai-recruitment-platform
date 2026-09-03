from app.core.config import settings

def test_openai_api_key_loaded():
    assert settings.OPENAI_API_KEY

def test_gemini_api_key_loaded():
    assert settings.GEMINI_API_KEY

def test_database_url_loaded():
    assert settings.DATABASE_URL