import pytest
from pydantic import ValidationError
from config import Settings, normalize_database_url


def test_settings_validation_missing_fields():
    # Testa se campos obrigatórios ausentes disparam ValidationError
    with pytest.raises(ValidationError):
        Settings(_env_file=None, database_url=None, google_api_key=None)


def test_settings_valid():
    # Testa carregamento correto com valores simulados válidos
    settings = Settings(
        _env_file=None,
        database_url="postgresql://postgres:postgres@localhost:5432/rag",
        google_api_key="mock-key",
        google_embedding_model="models/embedding-001",
        google_chat_model="gemini-2.5-flash-lite",
        pg_vector_collection_name="test_collection",
        pdf_path="data/document.pdf",
    )
    assert settings.database_url == "postgresql://postgres:postgres@localhost:5432/rag"
    assert settings.google_api_key == "mock-key"
    assert settings.google_embedding_model == "models/embedding-001"
    assert settings.google_chat_model == "gemini-2.5-flash-lite"
    assert settings.pg_vector_collection_name == "test_collection"
    assert settings.pdf_path == "data/document.pdf"
    assert settings.ingest_batch_size == 5
    assert settings.ingest_batch_pause_seconds == 10.0



def test_normalize_database_url():
    url_postgresql = "postgresql://user:pass@localhost/db"
    normalized = normalize_database_url(url_postgresql)
    assert normalized == "postgresql+psycopg://user:pass@localhost/db"

    url_already_normalized = "postgresql+psycopg://user:pass@localhost/db"
    assert normalize_database_url(url_already_normalized) == url_already_normalized

    url_other = "sqlite:///test.db"
    assert normalize_database_url(url_other) == url_other
