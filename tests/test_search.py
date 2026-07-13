from unittest.mock import MagicMock, patch
from search import _retrieve_context, search_prompt


def test_retrieve_context():
    # Mock de documentos retornados pelo banco vetorial
    doc1 = MagicMock()
    doc1.page_content = "Conteúdo do documento 1"
    doc2 = MagicMock()
    doc2.page_content = "Conteúdo do documento 2"

    mock_results = [(doc1, 0.1), (doc2, 0.2)]

    mock_vectorstore = MagicMock()
    mock_vectorstore.similarity_search_with_score.return_value = mock_results

    context = _retrieve_context("pergunta teste", mock_vectorstore)

    assert "Conteúdo do documento 1" in context
    assert "Conteúdo do documento 2" in context
    mock_vectorstore.similarity_search_with_score.assert_called_once_with("pergunta teste", k=10)


@patch("search.get_vectorstore")
@patch("search.ChatGoogleGenerativeAI")
def test_search_prompt_chain_creation(mock_llm_cls, mock_get_vectorstore):
    # Mock do vectorstore
    mock_vectorstore = MagicMock()
    mock_get_vectorstore.return_value = mock_vectorstore

    # Criação da chain
    chain = search_prompt()

    assert chain is not None
    mock_get_vectorstore.assert_called_once()
    mock_llm_cls.assert_called_once()
