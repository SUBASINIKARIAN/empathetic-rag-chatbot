# Empathetic RAG Chatbot

A production-grade multi-turn conversational AI chatbot that lets users query operational documents using natural language. Uses RAG (Pinecone vector search) + Google Gemini for reasoning, with conversation memory, empathetic tone detection, and encrypted API key storage.

## Features
- Multi-turn conversation with memory
- Tone detection (frustrated / confused / neutral) with adaptive responses
- Query rewriting for better retrieval
- Pinecone vector search (top-5 chunk retrieval)
- Cosine similarity grounding score (hallucination risk detection)
- Encrypted API keys at rest (Fernet symmetric encryption)
- Thumbs up/down feedback loop
- FastAPI backend + Streamlit frontend

## Tech Stack
| Layer | Tool |
|-------|------|
| LLM | Google Gemini API (gemini-1.5-flash) — free tier |
| Vector Search | Pinecone (free Starter tier) |
| Backend | FastAPI |
| Frontend | Streamlit |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Security | Fernet encrypted API keys |
| Evaluation | Cosine similarity scoring |

## Setup

### 1. Clone and configure environment
```bash
git clone https://github.com/SUBASINIKARIAN/empathetic-rag-chatbot.git
cd empathetic-rag-chatbot
cp .env.example .env
# Fill in GEMINI_API_KEY and PINECONE_API_KEY in .env
```

Get your free API keys:
- **Gemini**: aistudio.google.com → Get API Key
- **Pinecone**: pinecone.io → Sign up (free Starter) → API Keys

### 2. Install dependencies
```bash
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

### 3. Encrypt your API keys
```bash
python backend/key_manager.py
# This reads .env, encrypts it into .env.encrypted, and saves .secret.key
# Both files are gitignored — never committed
```

### 4. Ingest knowledge base into Pinecone
```bash
python data/index_documents.py
```

### 5. Start the backend
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 6. Start the frontend (new terminal)
```bash
streamlit run frontend/streamlit_app.py
```

## Project Structure
```
empathetic-rag-chatbot/
├── backend/
│   ├── main.py            # FastAPI app
│   ├── gemini_client.py   # Multi-turn chat with Gemini
│   ├── key_manager.py     # Fernet encryption for API keys
│   ├── retriever.py       # Pinecone vector search
│   ├── embedder.py        # SentenceTransformer embeddings
│   ├── tone_detector.py   # Frustration/confusion detection
│   ├── query_rewriter.py  # LLM-based query rewriting
│   ├── evaluator.py       # Cosine similarity scoring
│   └── requirements.txt
├── frontend/
│   ├── streamlit_app.py   # Chat UI with feedback buttons
│   └── requirements.txt
├── data/
│   ├── knowledge_base.json   # Documents to index
│   └── index_documents.py    # One-time ingestion script
├── .env.example
├── .gitignore             # .env, .secret.key, .env.encrypted are gitignored
└── README.md
```

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat` | Send a message, get AI response |
| POST | `/feedback` | Submit thumbs up/down rating |
| DELETE | `/session/{id}` | Clear conversation history |
| GET | `/health` | Health check |

## Security
API keys are encrypted at rest using Fernet (AES-128-CBC + HMAC-SHA256).
The encryption key (`.secret.key`) and encrypted env (`.env.encrypted`) are both gitignored.
