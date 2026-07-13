import sys
from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str
    google_api_key: str
    google_embedding_model: str = "models/embedding-001"
    google_chat_model: str = "gemini-2.5-flash-lite"
    pg_vector_collection_name: str = "pdf_documents"
    pdf_path: str = "data/document.pdf"
    ingest_batch_size: int = 5
    ingest_batch_pause_seconds: float = 10.0


# Inicialização e validação das configurações
try:
    settings = Settings()
except ValidationError as e:
    print("Erro de validação das configurações (variáveis de ambiente):")
    for error in e.errors():
        loc = " -> ".join(str(l) for l in error["loc"])
        print(f"  - {loc}: {error['msg']}")
    sys.exit(1)

DATABASE_URL = settings.database_url
GOOGLE_API_KEY = settings.google_api_key
GOOGLE_EMBEDDING_MODEL = settings.google_embedding_model
GOOGLE_CHAT_MODEL = settings.google_chat_model
PG_VECTOR_COLLECTION_NAME = settings.pg_vector_collection_name
PDF_PATH = settings.pdf_path
INGEST_BATCH_SIZE = settings.ingest_batch_size
INGEST_BATCH_PAUSE_SECONDS = settings.ingest_batch_pause_seconds



def normalize_database_url(url: str) -> str:
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


# Mantido para retrocompatibilidade
def validate_ingest_config() -> None:
    pass


# Mantido para retrocompatibilidade
def validate_search_config() -> None:
    pass
