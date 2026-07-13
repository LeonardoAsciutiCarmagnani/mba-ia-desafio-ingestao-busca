import sys
import time
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import (
    DATABASE_URL,
    INGEST_BATCH_PAUSE_SECONDS,
    INGEST_BATCH_SIZE,
    PDF_PATH,
    PG_VECTOR_COLLECTION_NAME,
    normalize_database_url,
    validate_ingest_config,
)
from vectorstore import get_embeddings



def ingest_pdf() -> None:
    validate_ingest_config()

    pdf_path = Path(PDF_PATH)
    if not pdf_path.exists():
        print(f"PDF não encontrado: {pdf_path.resolve()}")
        sys.exit(1)

    print(f"Carregando PDF: {pdf_path}")
    documents = PyPDFLoader(str(pdf_path)).load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n\n", "\n", " ", ""],
    )

    chunks = splitter.split_documents(documents)

    print(f"Indexando {len(chunks)} chunks no PostgreSQL...")
    embeddings = get_embeddings()
    connection = normalize_database_url(DATABASE_URL)

    try:
        vectorstore = None
        for i in range(0, len(chunks), INGEST_BATCH_SIZE):
            batch = chunks[i : i + INGEST_BATCH_SIZE]
            batch_num = i // INGEST_BATCH_SIZE + 1
            total_batches = (len(chunks) + INGEST_BATCH_SIZE - 1) // INGEST_BATCH_SIZE

            if i > 0:
                time.sleep(INGEST_BATCH_PAUSE_SECONDS)

            print(f"Lote {batch_num}/{total_batches} ({len(batch)} chunks)...")

            if vectorstore is None:
                vectorstore = PGVector.from_documents(
                    documents=batch,
                    embedding=embeddings,
                    collection_name=PG_VECTOR_COLLECTION_NAME,
                    connection=connection,
                    use_jsonb=True,
                    pre_delete_collection=True,
                )
            else:
                vectorstore.add_documents(batch)
    except Exception as exc:
        error = str(exc).lower()
        if "429" in error or "quota" in error or "rate" in error:
            print(f"Erro de quota/rate limit na API Gemini: {exc}")
            print("Aguarde ~1 minuto e execute novamente: python src/ingest.py")
        else:
            print(f"Erro ao indexar no banco: {exc}")
            print("Verifique se o PostgreSQL está rodando: docker compose up -d")
        sys.exit(1)

    print(f"Ingestão concluída: {len(chunks)} chunks indexados.")


if __name__ == "__main__":
    ingest_pdf()
