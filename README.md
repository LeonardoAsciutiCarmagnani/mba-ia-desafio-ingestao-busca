# MBA Engenharia de Software com IA - RAG Ingestão e Busca

Este é um projeto RAG (Retrieval-Augmented Generation) simples e modular desenvolvido em Python. Ele permite a ingestão de documentos PDF no banco de dados PostgreSQL (utilizando a extensão **pgVector**) e oferece uma interface interativa via CLI (linha de comando) para realizar buscas semânticas e responder perguntas com base no contexto do documento ingerido.

---

## 🛠️ Tecnologias Utilizadas

*   **Linguagem:** Python 3.11+
*   **Orquestração de IA:** LangChain (`langchain`, `langchain-community`, `langchain-core`)
*   **Provedor de LLM:** Google Gemini API (`langchain-google-genai`)
*   **Banco de Dados:** PostgreSQL com a extensão **pgvector** (`langchain-postgres` + `psycopg3`)
*   **Validação de Configurações:** `pydantic` e `pydantic-settings`
*   **Ambiente Conteinerizado:** Docker e Docker Compose
*   **Suíte de Testes:** `pytest`

---

## 📂 Estrutura do Projeto

```text
├── data/
│   └── document.pdf              # PDF que será ingerido
├── src/
│   ├── config.py                 # Validação declarativa das variáveis com Pydantic
│   ├── vectorstore.py            # Inicialização de embeddings (REST) e do vector store
│   ├── ingest.py                 # Fluxo de ingestão em lotes para o PostgreSQL
│   ├── search.py                 # Definição do RAG Prompt e Cadeia LCEL (REST)
│   └── chat.py                   # Interface CLI para interação com o usuário
├── tests/
│   ├── test_config.py            # Testes de configurações e normalizações
│   └── test_search.py            # Testes com mock da busca semântica
├── docker-compose.yml            # Infraestrutura de banco de dados
├── pytest.ini                    # Configurações do ambiente do pytest (pythonpath)
├── requirements.txt              # Dependências do projeto
├── .env.example                  # Template do arquivo de variáveis de ambiente
└── .gitignore                    # Arquivos ignorados pelo git
```

---

## 🚀 Como Executar o Projeto

Siga os passos abaixo para preparar o ambiente e rodar o projeto.

### 1. Criar e Ativar o Ambiente Virtual

No terminal da raiz do projeto, crie a pasta do ambiente virtual e ative-a:

**No Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**No Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar as Dependências

Instale os pacotes definidos no arquivo de requisitos:
```bash
pip install -r requirements.txt
```

### 3. Configurar as Variáveis de Ambiente

Copie o arquivo de exemplo de ambiente e preencha as suas chaves:

**No Windows:**
```cmd
copy .env.example .env
```

**No Linux/macOS:**
```bash
cp .env.example .env
```

Abra o arquivo `.env` gerado e defina a sua `GOOGLE_API_KEY`. As variáveis de controle de taxa (Rate Limit) já vêm pré-configuradas com limites mais suaves para a API Gemini (Free Tier):

| Variável | Descrição | Padrão |
| :--- | :--- | :--- |
| `GOOGLE_API_KEY` | Chave de acesso da API Gemini (Google AI Studio) | *Obrigatório* |
| `GOOGLE_EMBEDDING_MODEL` | Modelo usado para gerar os vetores de busca | `'models/gemini-embedding-001'` |
| `GOOGLE_CHAT_MODEL` | Modelo LLM usado para responder as perguntas | `'gemini-2.5-flash-lite'` |
| `DATABASE_URL` | String de conexão para o PostgreSQL | `'postgresql://postgres:postgres@localhost:5432/rag'` |
| `PG_VECTOR_COLLECTION_NAME`| Nome da coleção onde os vetores serão armazenados | `'documents'` |
| `PDF_PATH` | Caminho do arquivo PDF a ser ingerido | `'data/document.pdf'` |
| `INGEST_BATCH_SIZE` | Quantidade de chunks inseridos por lote | `5` |
| `INGEST_BATCH_PAUSE_SECONDS`| Segundos de intervalo entre lotes na ingestão | `10.0` |

### 4. Subir a Infraestrutura (Docker)

Suba o container do PostgreSQL e pgvector:
```bash
docker compose up -d
```
> **Nota:** O `docker-compose` inclui um serviço bootstrap que aguarda a inicialização e executa automaticamente o comando `CREATE EXTENSION IF NOT EXISTS vector;` no banco, deixando-o 100% pronto.

### 5. Ingerir o PDF no Banco de Dados

Para processar o PDF localizado no caminho configurado (por padrão `data/document.pdf`) e criar os vetores no banco de dados, execute:
```bash
python src/ingest.py
```
Esse processo dividirá o documento em pedaços (chunks) menores e fará o envio em lotes respeitando as pausas configuradas no `.env` para evitar o erro `429 (Rate Limit)`.

### 6. Executar o Chat Interativo (CLI)

Agora você pode conversar com os dados do documento fazendo perguntas no terminal:
```bash
python src/chat.py
```

*Exemplo de interação:*
```text
Faça sua pergunta:
PERGUNTA: Qual o ano de fundação da empresa Alfa Telecom?
RESPOSTA: 1987
---
PERGUNTA: Qual a capital da França?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
```
Digite `sair` ou `exit` para encerrar.

---

## 🧪 Testes Automatizados

O projeto utiliza o `pytest` para a execução de testes unitários offline.

Para executar os testes:
```bash
pytest
```
*   **Configuração de PYTHONPATH:** Graças ao arquivo `pytest.ini`, o pytest adiciona automaticamente a pasta `src/` ao caminho de busca do Python, evitando erros de importação nos testes.

---

## 💡 Soluções de Problemas Comuns

### ⚠️ Erro de Quota (429 Rate Limit) da API do Gemini
Se encontrar o erro `429: You exceeded your current quota` durante a ingestão do PDF, ajuste as variáveis abaixo no `.env` para diminuir a taxa de requisições:
```ini
INGEST_BATCH_SIZE=3
INGEST_BATCH_PAUSE_SECONDS=15
```

### ❌ Avisos de Importação Não Resolvidos na IDE (VS Code / PyCharm)
Como o Python adiciona o diretório de execução dos scripts ao caminho principal e as importações são feitas de forma direta (ex: `from config import ...`), as IDEs podem mostrar avisos visuais. Resolva isso da seguinte forma:

*   **No VS Code:** Crie uma pasta `.vscode` e um arquivo `settings.json` na raiz com o seguinte conteúdo:
    ```json
    {
      "python.analysis.extraPaths": ["./src"]
    }
    ```
*   **No PyCharm:** Clique com o botão direito na pasta `src/` e selecione **Mark Directory as -> Sources Root**.
