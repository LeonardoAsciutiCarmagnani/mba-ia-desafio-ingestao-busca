from typing import Any, Optional

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_postgres import PGVector

from config import GOOGLE_API_KEY, GOOGLE_CHAT_MODEL, validate_search_config
from vectorstore import get_vectorstore

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def _retrieve_context(question: str, vectorstore: PGVector) -> str:
    results = vectorstore.similarity_search_with_score(question, k=10)
    return "\n\n".join(doc.page_content for doc, _score in results)


def search_prompt(question: Optional[str] = None) -> Optional[Runnable]:
    try:
        validate_search_config()
        vectorstore = get_vectorstore()
        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        llm = ChatGoogleGenerativeAI(
            model=GOOGLE_CHAT_MODEL,
            google_api_key=GOOGLE_API_KEY,
            temperature=0,
            transport="rest",
        )


        chain = (
            RunnablePassthrough.assign(
                contexto=lambda x: _retrieve_context(x["pergunta"], vectorstore),
            )
            | prompt
            | llm
            | StrOutputParser()
        )

        if question is not None:
            return chain.invoke({"pergunta": question})

        return chain
    except Exception as exc:
        print(f"Erro ao inicializar a busca: {exc}")
        return None

