# Empathetic RAG Chatbot

A production-grade multi-turn conversational AI chatbot that lets users query operational databases and documents using natural language. Uses RAG (vector search) + Claude for reasoning, with conversation memory and empathetic tone detection.

## Features
- Multi-turn conversation with memory
- Tone detection (frustrated / confused / neutral) with adaptive responses
- Query rewriting for better retrieval
- Pinecone vector search (top-5 chunk retrieval)
- Cosine similarity grounding score (hallucination risk detection)
- Thumbs up/down feedback loop
- FastAPI backend + Streamlit frontend

## Tech Stack
| Layer | Tool |
|-------|------|
| LLM | Claude API (claude-sonnet-4-20250514) |
| Vector Search | Pinecone |
| Backend | FastAPI |
| Frontend | Streamlit |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Evaluation | Cosine similarity scoring |

## Setup

### 1. Clone and configure environment
```bash
git clone https://github.com/SUBASINIKARIAN/empathetic-rag-chatbot.git
cd empathetic-rag-chatbot
cp .env.example .env
# Fill in ANTHROPIC_API_KEY and PINECONE_API_KEY in .env
```

### 2. Install backend dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Ingest knowledge base into Pinecone
```bash
cd data
python index_documents.py
```

### 4. Start the backend
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 5. Start the frontend (new terminal)
```bash
cd frontend
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Project Structure
```
empathetic-rag-chatbot/
├── backend/
│   ├── main.py            # FastAPI app
│   ├── claude_client.py   # Multi-turn chat orchestration
│   ├── retriever.py       # Pinecone vector search
│   ├── embedder.py        # SentenceTransformer embeddings
│   ├── tone_detector.py   # Frustration/confusion detection
│   ├── query_rewriter.py  # LLM-based query rewriting
│   ├── evaluator.py       # Cosine similarity scoring
│   └── requirements.txt
├── frontend/
│   ├── streamlit_app.py   # Chat UI
│   └── requirements.txt
├── data/
│   ├── knowledge_base.json   # Documents to index
│   └── index_documents.py    # One-time ingestion script
├── .env.example
└── README.md
```

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat` | Send a message, get AI response |
| POST | `/feedback` | Submit thumbs up/down rating |
| DELETE | `/session/{id}` | Clear conversation history |
| GET | `/health` | Health check |
