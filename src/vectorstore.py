from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

from config import (
    DATABASE_URL,
    GOOGLE_API_KEY,
    GOOGLE_EMBEDDING_MODEL,
    PG_VECTOR_COLLECTION_NAME,
    normalize_database_url,
)


def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    return GoogleGenerativeAIEmbeddings(
        model=GOOGLE_EMBEDDING_MODEL,
        google_api_key=GOOGLE_API_KEY,
        transport="rest",
    )



def get_vectorstore() -> PGVector:
    return PGVector(
        embeddings=get_embeddings(),
        collection_name=PG_VECTOR_COLLECTION_NAME,
        connection=normalize_database_url(DATABASE_URL),
        use_jsonb=True,
    )
