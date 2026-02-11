# 🏥 BPJS RAG Intelligence System (Omnichannel Support)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-High_Performance-009688?logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-AI_Framework-33A3F5?logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/AI-Gemini_2.5_Flash-4285F4?logo=google&logoColor=white)
![ChromaDB](https://img.shields.io/badge/Vector_DB-ChromaDB-FF6B35)
![Telegram API](https://img.shields.io/badge/Interface-Telegram_Bot-2CA5E0?logo=telegram&logoColor=white)

---

## 📋 Table of Contents

1. [Executive Summary](#executive-summary)
2. [Project Architecture](#project-architecture)
3. [Tech Stack & Dependencies](#tech-stack--dependencies)
4. [Project Structure & File Organization](#project-structure--file-organization)
5. [How the Code Works - Data Flow](#how-the-code-works---data-flow)
6. [Detailed Component Breakdown](#detailed-component-breakdown)
7. [Installation & Setup Guide](#installation--setup-guide)
8. [How to Run the Project](#how-to-run-the-project)
9. [API Endpoints & Usage](#api-endpoints--usage)
10. [File Dependencies & Linking](#file-dependencies--linking)
11. [Troubleshooting](#troubleshooting)

---

## Executive Summary

**BPJS RAG Intelligence System** adalah solusi Enterprise-grade AI yang mengotomatisasi layanan informasi BPJS Kesehatan dengan dua antarmuka: **Web Chat** dan **Telegram Bot**. 

Sistem ini menggunakan arsitektur **Retrieval-Augmented Generation (RAG)** untuk meminimalkan halusinasi AI dengan mengambil rujukan langsung dari dokumen BPJS resmi dalam format PDF. Backend dibangun dengan **FastAPI** yang mendukung concurrency tinggi menggunakan Asynchronous Background Tasks.

**Key Benefits:**
- ✅ Omnichannel Support: Satu backend melayani Web & Telegram
- ✅ Akurat: Jawaban berbasis dokumen resmi BPJS
- ✅ Scalable: Async processing dengan background tasks
- ✅ Modular: Pemisahan tegas antara Core Logic, Data, dan Frontend

---

## Project Architecture

### System Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA INGESTION PHASE                      │
├─────────────────────────────────────────────────────────────┤
│  PDF Files (BPJS Docs)                                       │
│        ↓ (IngestionService)                                  │
│  Text Extraction & Chunking (RecursiveCharacterTextSplitter) │
│        ↓                                                      │
│  Embeddings Generation (Google Gemini Embeddings)            │
│        ↓                                                      │
│  ChromaDB (Vector Store - Persistent Storage)                │
└─────────────────────────────────────────────────────────────┘
                           ↑
                    (Offline Process)
                           │
┌─────────────────────────────────────────────────────────────┐
│                   RUNTIME INFERENCE PHASE                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  User Query Input                                            │
│    ├─→ Web Frontend (index.html + script.js)                 │
│    └─→ Telegram Bot (@BotFather created)                     │
│           ↓                                                  │
│           FastAPI Gateway (telegram/web front-end/main.py)  │
│           ├─→ POST /chat (REST API)                         │
│           └─→ Webhook Handler /webhook/telegram (Event)     │
│                  ↓                                           │
│           ChatService (src/services/chat_service.py)        │
│           ├─→ RAGService (Retrieval)                        │
│           │   └─→ Chromadb.search(query, k=3)              │
│           ├─→ Prompt Template Construction                 │
│           └─→ LLM Inference (Gemini 2.5 Flash)             │
│                  ↓                                           │
│           Structured Response (ChatResponse Schema)         │
│           ├─→ answer (AI Response)                          │
│           └─→ sources (Retrieved Documents)                 │
│                  ↓                                           │
│           Return to User (JSON/Telegram Message)            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Request Flow Sequence

```
[User] 
  ├─ Web Chat: GET http://localhost:8000 → bot.html
  │            POST /chat → JSON Response
  │
  └─ Telegram: /start command → FastAPI Webhook
               Message Text → Background Task → Telegram API
```

---

## Tech Stack & Dependencies

### Core Framework
- **FastAPI** - Web framework for API & webhook handling
- **Uvicorn** - ASGI server (high-performance HTTP server)
- **Pydantic** - Data validation & serialization

### AI/ML Stack
- **LangChain** - Orchestration framework for LLM
  - `langchain_core` - Base abstractions
  - `langchain_google_genai` - Google Gemini integration
  - `langchain_community` - PDF loader & integrations
  - `langchain_text_splitters` - Document chunking
  - `langchain_chroma` - ChromaDB wrapper
- **Google Generative AI (Gemini)** - LLM model & embeddings
- **ChromaDB** - Vector database for semantic search

### Data Processing
- **PyPDF** - PDF text extraction
- **python-dotenv** - Environment variable management
- **PyYAML** - Prompt configuration parsing

### Telegram Integration
- **httpx** - Async HTTP client for Telegram API calls

### Development & Utilities
- **tqdm** - Progress bars for data loading
- **pydantic-settings** - Configuration management from .env

---

## Project Structure & File Organization

```
bpjs_screening_report_generator/
│
├── 📄 README.md                          # Project documentation
├── 📄 .env                               # Environment variables (API keys, tokens)
├── 📄 .gitignore                         # Git ignore rules
├── 📄 environment.yml                    # Conda dependencies (alternative to pip)
├── 📄 __init__.py                        # Python package marker
│
├── 📁 config/
│   └── 📄 prompts.yaml                   # System prompt & instructions
│
├── 📁 data/                              # Data persistence layer
│   ├── 📁 raw_docs/                      # [INPUT] PDF files go here
│   ├── 📁 vector_store/                  # [OUTPUT] ChromaDB embeddings
│   │   ├── 📄 chroma.sqlite3             # Vector database
│   │   └── 📁 [uuid]/                    # Collection metadata
│   └── 📁 chunks/                        # Temporary chunked documents
│
├── 📁 src/                               # Core business logic
│   ├── 📄 __init__.py                    # Package marker
│   │
│   ├── 📁 core/                          # Configuration & utilities
│   │   ├── 📄 config.py                  # Settings & paths (pydantic)
│   │   ├── 📄 logger.py                  # Logging configuration
│   │   └── 📄 __init__.py
│   │
│   ├── 📁 domain/                        # Data models & schemas
│   │   ├── 📄 schemas.py                 # Pydantic models (ChatRequest, ChatResponse)
│   │   └── 📄 __init__.py
│   │
│   └── 📁 services/                      # AI/ML services
│       ├── 📄 ingestion_service.py       # Document → Vector DB pipeline
│       ├── 📄 rag_service.py             # Retrieval Augmented Generation
│       ├── 📄 chat_service.py            # Conversation orchestration
│       └── 📄 __init__.py
│
├── 📁 web front-end/                     # Web interface
│   ├── 📄 main.py                        # FastAPI server (web route)
│   ├── 📄 index.html                     # Chat UI (HTML template)
│   ├── 📄 bot.html                       # Alternative chat template
│   ├── 📄 script.js                      # Frontend logic & API calls
│   └── 📄 __pycache__/
│
├── 📁 telegram front-end/                # Telegram webhook handler
│   ├── 📄 main.py                        # FastAPI server + webhook
│   └── 📄 __pycache__/
│
└── 📁 lab/                               # Development & experiments
    ├── 📄 notebook.ipynb                 # Jupyter notebook for testing
    └── 📄 __pycache__/
```

---

## How the Code Works - Data Flow

### **Phase 1: Data Ingestion (Offline - Run Once)**

**Trigger:** `python -m src.services.ingestion_service`

```
Step 1: Load PDFs
├─ ingestion_service.load_pdfs()
│  ├─ Scans: data/raw_docs/
│  ├─ Uses: PyPDFLoader (LangChain)
│  └─ Returns: List[Document] with content & metadata
│
Step 2: Split Documents
├─ ingestion_service.split_documents(raw_docs)
│  ├─ RecursiveCharacterTextSplitter(
│  │   chunk_size=1000,
│  │   chunk_overlap=200
│  │ )
│  └─ Returns: List[Document] with smaller chunks
│
Step 3: Generate Embeddings & Save
├─ ingestion_service.save_to_chroma(chunks)
│  ├─ GoogleGenerativeAIEmbeddings()
│  ├─ Chroma.from_documents()
│  └─ Persists to: data/vector_store/
│
✅ Result: Vector DB ready for retrieval
```

**Key Files:**
- [`src/services/ingestion_service.py`](src/services/ingestion_service.py) - Main orchestrator
- [`src/core/config.py`](src/core/config.py) - Paths & settings

---

### **Phase 2: Chat/Query Processing (Runtime - Multiple Invocations)**

#### **2A: Web Interface Flow**

```
User Browser
    ↓
GET http://localhost:8000/
    ↓
[web front-end/main.py] → FastAPI serves [index.html] + [script.js]
    ↓
User types query → Click "Send"
    ↓
[script.js] executes:
    POST /chat
    Content-Type: application/json
    {
        "query": "Berapa iuran BPJS per bulan?",
        "session_id": "web-user-123"
    }
    ↓
[web front-end/main.py::handle_bpjs_chat()]
    ├─ Receives ChatRequest
    ├─ Calls chat_service.generate_response()
    ├─ Returns ChatResponse (answer + sources)
    ↓
[script.js] renders response in UI
    ↓
Browser displays answer + source citations
```

**Key Files:**
- [`web front-end/main.py`](web%20front-end/main.py) - FastAPI routes
- [`web front-end/index.html`](web%20front-end/index.html) - Chat UI
- [`web front-end/script.js`](web%20front-end/script.js) - Frontend logic

---

#### **2B: Telegram Bot Flow**

```
User sends message to Telegram Bot
    ↓
Telegram Servers detect update
    ↓
POST https://your-ngrok-url/webhook/telegram
    ↓
[telegram front-end/main.py::telegram_webhook()]
    ├─ Extracts: text, chat_id, username
    ├─ Validates message exists
    ├─ background_tasks.add_task(process_telegram_message, ...)
    └─ Returns {"status": "received"} immediately (no timeout)
    ↓
[async process_telegram_message()] runs in background
    ├─ Sends "typing" action to Telegram
    ├─ Calls chat_service.generate_response()
    │  └─ session_id = f"tg-{chat_id}"
    ├─ Parses response (answer + sources)
    └─ Sends reply back via Telegram API
    ↓
User sees bot reply in chat
```

**Key Files:**
- [`telegram front-end/main.py`](telegram%20front-end/main.py) - Webhook handler
- `.env` - Contains `TELEGRAM_BOT_TOKEN`

---

### **Phase 3: Core AI Logic (Common for Both Interfaces)**

```
[ChatService.generate_response(query, session_id)]
│
├─→ Step 1: Retrieve Context from Vector DB
│   ├─ rag_service.search(query=query, k=3)
│   ├─ ChromaDB semantic search
│   │  ├─ Embeds query using Google Gemini Embeddings
│   │  ├─ Finds 3 most similar chunks
│   │  └─ Returns List[Document]
│   ├─ rag_service.format_docs(docs)
│   └─ context_text = "Doc 1: ...\nDoc 2: ...\nDoc 3: ..."
│
├─→ Step 2: Build Prompt with Context
│   ├─ ChatPromptTemplate construction:
│   │  ├─ system: "Kamu adalah asisten AI yang membantu..."
│   │  ├─ chat_history: (previous messages for session)
│   │  ├─ user_input: "Context: {context}\n\nQuestion: {query}"
│   │  └─ model: Gemini 2.5 Flash
│   ├─ get_session_history(session_id)
│   │  └─ Stores conversation in ChatMessageHistory dict
│   └─ Build full prompt with context
│
├─→ Step 3: Generate LLM Response
│   ├─ llm.invoke(prompt)
│   ├─ Temperature: 0.3 (low randomness, factual)
│   └─ Returns: AI answer string
│
├─→ Step 4: Package Response
│   ├─ ChatResponse schema:
│   │  ├─ answer: "Iuran BPJS untuk..."
│   │  └─ sources: "📄 Panduan Layanan JKN-KIS-6-96.pdf"
│   └─ Return to caller
│
└─→ Result: User sees answer with citations
```

**Key Files:**
- [`src/services/chat_service.py`](src/services/chat_service.py) - Orchestrator
- [`src/services/rag_service.py`](src/services/rag_service.py) - Vector retrieval
- [`src/domain/schemas.py`](src/domain/schemas.py) - Data models
- [`config/prompts.yaml`](config/prompts.yaml) - System instructions

---

## Detailed Component Breakdown

### 1. **Configuration Layer** (`src/core/config.py`)

```
Purpose: Centralized settings management
├─ Load environment variables from .env
├─ Define base paths:
│  ├─ BASE_DIR = project root
│  ├─ DATA_DIR = data folder
│  ├─ PROMPT_DIR = prompts.yaml
│  └─ CHROMA_PERSIST_DIR = vector store
├─ API credentials:
│  ├─ GOOGLE_API_KEY (for Gemini)
│  ├─ GENAI_MODEL (default: models/gemini-2.5-flash)
│  └─ EMBEDDING_MODEL (default: models/gemini-embedding-001)
└─ Singleton: settings = Settings()
```

**Usage Pattern:**
```python
from src.core.config import settings
pdf_dir = settings.DATA_DIR / "raw_docs"
api_key = settings.GOOGLE_API_KEY
```

---

### 2. **Logging Layer** (`src/core/logger.py`)

```
Purpose: Structured logging across services
├─ get_logger(name) → returns Logger instance
├─ Logs to console with timestamps & levels
├─ Used by all services (IngestionService, ChatService, etc.)
└─ Helps debugging during development
```

---

### 3. **Data Schemas** (`src/domain/schemas.py`)

```
Pydantic Models (Data Validation):

ChatRequest:
├─ query: str          # User question
└─ session_id: str     # Conversation ID

ChatResponse:
├─ answer: str         # AI response
└─ sources: str        # Retrieved document references

Benefits:
├─ Automatic validation
├─ OpenAPI documentation
└─ Type safety
```

---

### 4. **Ingestion Service** (`src/services/ingestion_service.py`)

```
Responsibility: PDF → Vector DB pipeline

Methods:
├─ __init__()
│  ├─ Initializes logger
│  ├─ Sets paths (pdf_dir, db_dir)
│  └─ Configures chunking (1000 chars, 200 overlap)
│
├─ load_pdfs() → List[Document]
│  ├─ Scans data/raw_docs/ for PDF files
│  ├─ Uses PyPDFLoader for each file
│  ├─ Extracts text + metadata
│  └─ Returns documents with source attribution
│
├─ split_documents(docs) → List[Document]
│  ├─ RecursiveCharacterTextSplitter
│  ├─ Splits by character limits
│  ├─ Preserves overlaps for context
│  └─ Returns smaller chunks
│
├─ save_to_chroma(chunks)
│  ├─ Initializes GoogleGenerativeAIEmbeddings
│  ├─ Clears old vector store if exists
│  ├─ Embeds all chunks
│  └─ Persists to ChromaDB
│
└─ run() → Full pipeline
   ├─ load_pdfs() → split_documents() → save_to_chroma()
   └─ Logs progress & errors
```

---

### 5. **RAG Service** (`src/services/rag_service.py`)

```
Responsibility: Retrieve relevant documents from vector DB

Methods:
├─ __init__()
│  ├─ Loads ChromaDB from persistent storage
│  ├─ Initializes embeddings model
│  └─ Creates retriever (k=3 default)
│
├─ search(query: str, k: int) → List[Document]
│  ├─ Embeds user query (same model as ingestion)
│  ├─ Semantic search in ChromaDB
│  ├─ Returns top-k most similar chunks
│  └─ Includes metadata (page, source file)
│
└─ format_docs(docs) → str
   ├─ Concatenates all document contents
   ├─ Adds separators between documents
   └─ Ready for LLM prompt injection
```

---

### 6. **Chat Service** (`src/services/chat_service.py`)

```
Responsibility: Orchestrate conversation with context awareness

Key Concepts:
├─ Session Management
│  ├─ self.store: Dict[session_id, ChatMessageHistory]
│  ├─ Persists conversation per user
│  ├─ get_session_history(session_id)
│  └─ Enables multi-turn conversations
│
├─ Prompt Engineering
│  ├─ Loads system_instruction from config/prompts.yaml
│  ├─ ChatPromptTemplate with MessagesPlaceholder
│  ├─ Injects retrieved context
│  └─ Maintains message history
│
├─ LLM Integration
│  ├─ ChatGoogleGenerativeAI(model="gemini-2.5-flash")
│  ├─ Temperature=0.3 (factual, less creative)
│  ├─ RunnableWithMessageHistory for stateful chains
│  └─ StrOutputParser for string responses
│
└─ generate_response(query, session_id) → ChatResponse
   ├─ Retrieves context (RAG)
   ├─ Extracts sources from docs
   ├─ Formats prompt with context
   ├─ Gets session history
   ├─ Invokes LLM chain
   ├─ Extracts answer & sources
   └─ Returns ChatResponse object
```

---

### 7. **Web Frontend** (`web front-end/`)

```
index.html / bot.html:
├─ HTML structure
├─ CSS styling
├─ Container for messages
└─ Input field for user query

script.js:
├─ Event listeners on send button
├─ POST /chat API calls
├─ JSON parsing (request/response)
├─ DOM manipulation (append messages)
├─ Session ID generation/persistence
└─ Real-time message rendering
```

**Data Flow:**
```
User Input → script.js → POST /chat → FastAPI → ChatService → LLM
    ↑                                                           ↓
    ←─────────────────── Response JSON ←─────────────────────────
```

---

### 8. **Telegram Frontend** (`telegram front-end/main.py`)

```
Routes:
├─ GET /docs → OpenAPI docs
├─ POST /chat → Same as web (for testing)
└─ POST /webhook/telegram → Telegram event handler

Webhook Handler:
├─ Validates payload structure
├─ Extracts message text & chat_id
├─ Adds async task (no blocking)
├─ Returns immediately to Telegram
│
Background Task (process_telegram_message):
├─ Sends "typing" indicator to user
├─ Calls ChatService.generate_response()
├─ Formats response + sources
└─ Sends via Telegram API (httpx)
```

**Async Pattern:**
```
POST /webhook/telegram
    ↓
Return {"status": "received"} immediately
    ↓
Background task processes in parallel
    ↓
Send response to Telegram bot API
    ↓
User receives message
```

---

### 9. **Configuration Files**

#### `config/prompts.yaml`
```yaml
prompt: |
  Kamu adalah asisten AI yang membantu menjawab pertanyaan BPJS.
  Gunakan konteks dari dokumen untuk menjawab dengan akurat.
  Jika tidak tahu, katakan "Maaf, saya tidak menemukan informasi tersebut."
```

#### `.env` (Template)
```env
GOOGLE_API_KEY=your_google_ai_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
GENAI_MODEL=models/gemini-2.5-flash
EMBEDDING_MODEL=models/gemini-embedding-001
CHROMA_PATH=data/vector_store
```

---

## Installation & Setup Guide

### 1. Prerequisites

- **Python 3.10+** (tested on 3.10, 3.11, 3.12)
- **Google AI Studio API Key** (free tier available)
- **Telegram Bot Token** (from @BotFather on Telegram)
- **Git** (for cloning the repo)
- **ngrok** (for public URL tunneling - Telegram only)

### 2. Clone Repository

```bash
git clone https://github.com/yourusername/bpjs-screening-report-generator.git
cd bpjs_screening_report_generator
```

### 3. Environment Configuration

Create `.env` file in project root:

```env
# Google AI Credentials (for LLM & Embeddings)
GOOGLE_API_KEY=AIzaSy_YOUR_ACTUAL_KEY_HERE

# Telegram Credentials (for Telegram bot)
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# Model Configuration
GENAI_MODEL=models/gemini-2.5-flash
EMBEDDING_MODEL=models/gemini-embedding-001
CHROMA_PATH=data/vector_store
```

**How to get these keys:**

1. **Google API Key:**
   - Visit https://ai.google.dev/
   - Click "Get API Key"
   - Create new API key in Google Cloud Console
   - Copy and paste in `.env`

2. **Telegram Bot Token:**
   - Search @BotFather on Telegram
   - Send /start
   - Send /newbot
   - Follow prompts, choose bot name & username
   - Copy token to `.env`

### 4. Install Dependencies

```bash
# Option A: Using pip (Recommended)
pip install -r requirements.txt

# Or install manually:
pip install fastapi uvicorn[standard] httpx \
    langchain langchain-google-genai langchain-chroma chromadb \
    pydantic-settings python-multipart pyyaml tqdm

# Option B: Using conda (if using Conda environment)
conda env create -f environment.yml
conda activate bpjs
```

### 5. Prepare PDF Documents

Place BPJS regulation PDFs in:
```
data/raw_docs/
├── Panduan Layanan JKN-KIS.pdf
├── Peraturan Iuran BPJS.pdf
└── [other BPJS documents].pdf
```

---

## How to Run the Project

### **Step 1: Data Ingestion (One-time Setup)**

```bash
# Activate virtual environment (if using venv)
# source venv/bin/activate  # On Linux/Mac
# venv\Scripts\activate     # On Windows

# Run ingestion service
python -m src.services.ingestion_service
```

**Output:**
```
[IngestionService] === START INGESTION ===
[IngestionService] Ditemukan 3 file PDF.
[IngestionService] Processing: Panduan Layanan JKN-KIS.pdf
[IngestionService] Document split into 45 chunks
[IngestionService] Saving to ChromaDB...
[IngestionService] === FINISH INGESTION ===
```

**Result:** Vector embeddings saved to `data/vector_store/`

---

### **Step 2A: Run Web Interface**

```bash
cd "web front-end"
uvicorn main:app --reload --port 8000
```

**Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**Access:** Open browser → `http://localhost:8000`

---

### **Step 2B: Run Telegram Interface (Advanced)**

#### **2B.1: Setup ngrok (Local Testing)**

```bash
# Install ngrok from https://ngrok.com/download
# Then in new terminal:
ngrok http 8000
```

**Output:**
```
Session Status                online
Session Expires               1 hour, 59 minutes
Version                       3.x.x
Region                        us (United States)
Forwarding                    https://abc-123-def.ngrok.io -> http://localhost:8000
```

Copy the forwarding URL (e.g., `https://abc-123-def.ngrok.io`)

#### **2B.2: Set Telegram Webhook**

Open in browser:
```
https://api.telegram.org/bot<YOUR_TELEGRAM_BOT_TOKEN>/setWebhook?url=<YOUR_NGROK_URL>/webhook/telegram
```

Replace:
- `<YOUR_TELEGRAM_BOT_TOKEN>` with token from .env
- `<YOUR_NGROK_URL>` with ngrok URL above

**Example:**
```
https://api.telegram.org/bot123456:ABC-DEF1234ghIkl/setWebhook?url=https://abc-123-def.ngrok.io/webhook/telegram
```

**Response (if successful):**
```json
{"ok":true,"result":true,"description":"Webhook was set"}
```

#### **2B.3: Start Telegram Server**

```bash
cd "telegram front-end"
uvicorn main:app --reload --port 8000
```

#### **2B.4: Test with Your Bot**

- Open Telegram
- Find your bot (@your_bot_username)
- Send: `/start`
- Send: `Berapa iuran BPJS per bulan?`
- Bot responds with answer + sources

---

## API Endpoints & Usage

### **Endpoint 1: Chat (Web)**

```http
POST /chat
Content-Type: application/json

{
  "query": "Bagaimana cara daftar BPJS?",
  "session_id": "web-user-1"
}
```

**Response:**
```json
{
  "answer": "Untuk mendaftar BPJS, Anda dapat:\n1. Kunjungi kantor BPJS terdekat\n2. Bawa dokumen identitas...",
  "sources": "📄 Panduan Layanan JKN-KIS-6-96.pdf\n📄 Peraturan Pendaftaran BPJS.pdf"
}
```

---

### **Endpoint 2: Telegram Webhook**

```http
POST /webhook/telegram
Content-Type: application/json

{
  "message": {
    "message_id": 123,
    "date": 1234567890,
    "chat": {
      "id": 987654321,
      "username": "user123"
    },
    "text": "Berapa iuran BPJS?"
  }
}
```

**Response (Immediate):**
```json
{"status": "received"}
```

**Background Action:**
- Sends reply via Telegram API
- User receives bot message after ~1-2 seconds

---

### **Endpoint 3: API Documentation**

```
GET /docs
```

Opens interactive Swagger UI (FastAPI auto-generated)

---

## File Dependencies & Linking

### **Dependency Graph**

```
┌─ web front-end/main.py
│  └─ Imports:
│     ├─ src.services.chat_service::ChatService
│     ├─ src.domain.schemas::ChatRequest, ChatResponse
│     └─ src.core.config::settings
│
├─ telegram front-end/main.py
│  └─ Imports:
│     ├─ src.services.chat_service::ChatService
│     ├─ src.domain.schemas::ChatRequest, ChatResponse
│     └─ src.core.config::settings
│
├─ src/services/chat_service.py
│  └─ Imports:
│     ├─ src.services.rag_service::RAGService
│     ├─ src.core.config::settings
│     ├─ src.core.logger::get_logger
│     ├─ src.domain.schemas::ChatResponse
│     ├─ config/prompts.yaml
│     └─ langchain (for LLM & chains)
│
├─ src/services/rag_service.py
│  └─ Imports:
│     ├─ src.core.config::settings
│     ├─ src.core.logger::get_logger
│     └─ langchain_chroma::Chroma (persistence)
│
├─ src/services/ingestion_service.py
│  └─ Imports:
│     ├─ src.core.config::settings
│     ├─ src.core.logger::get_logger
│     ├─ data/raw_docs/ (reads PDFs)
│     └─ data/vector_store/ (writes embeddings)
│
├─ src/core/config.py
│  └─ Loads:
│     ├─ .env (environment variables)
│     └─ Defines paths to all resources
│
├─ src/core/logger.py
│  └─ Used by:
│     ├─ All services for logging
│     └─ FastAPI middleware
│
├─ src/domain/schemas.py
│  └─ Used by:
│     ├─ FastAPI for request/response validation
│     └─ Services for type safety
│
└─ config/prompts.yaml
   └─ Loaded by:
      └─ ChatService for system instructions
```

### **Data Flow Dependencies**

```
User Input (Web/Telegram)
    ↓
FastAPI main.py
    ├─→ Validates with schemas.ChatRequest
    ├─→ Calls ChatService.generate_response()
    │    ├─→ RAGService.search() queries ChromaDB
    │    │    └─ Loaded from: data/vector_store/
    │    ├─→ ChatService builds prompt from prompts.yaml
    │    ├─→ LLM inference (Gemini)
    │    └─→ Returns schemas.ChatResponse
    └─→ Response to user
```

### **File Read/Write Operations**

| File | Operation | Used By | Purpose |
|------|-----------|---------|---------|
| `.env` | Read | `src/core/config.py` | API keys & secrets |
| `config/prompts.yaml` | Read | `src/services/chat_service.py` | System instructions |
| `data/raw_docs/*.pdf` | Read | `src/services/ingestion_service.py` | Source documents |
| `data/vector_store/` | Read/Write | `src/services/rag_service.py` & `ingestion_service.py` | Vector DB persistence |
| `web front-end/index.html` | Serve | FastAPI | Chat UI |
| `web front-end/script.js` | Serve | Browser | Frontend logic |

---

## Troubleshooting

### **Issue 1: "GOOGLE_API_KEY not found"**

**Cause:** Missing `.env` file or incorrect key format

**Solution:**
```bash
# Verify .env exists in project root
ls -la | grep ".env"

# Check content
cat .env

# Ensure no extra spaces or quotes:
# ✅ Correct:   GOOGLE_API_KEY=AIzaSy_xxxxx
# ❌ Wrong:     GOOGLE_API_KEY = "AIzaSy_xxxxx"
```

---

### **Issue 2: "ChromaDB is empty" or "No documents found"**

**Cause:** Ingestion service hasn't been run

**Solution:**
```bash
# 1. Add PDFs to data/raw_docs/
cp your-bpjs-documents.pdf data/raw_docs/

# 2. Run ingestion
python -m src.services.ingestion_service

# 3. Verify vector store was created
ls -la data/vector_store/
```

---

### **Issue 3: "ModuleNotFoundError: No module named 'src'"**

**Cause:** Running from wrong directory

**Solution:**
```bash
# Make sure you're in project root, not subdirectories
pwd
# Should output: /path/to/bpjs_screening_report_generator

# Then run:
python -m src.services.ingestion_service

# Or add to Python path:
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

---

### **Issue 4: Telegram webhook not connecting**

**Cause:** ngrok URL expired or webhook not set properly

**Solution:**
```bash
# 1. Restart ngrok (generates new URL)
ngrok http 8000

# 2. Set webhook again with new URL
curl "https://api.telegram.org/bot<TOKEN>/setWebhook?url=<NEW_NGROK_URL>/webhook/telegram"

# 3. Verify webhook is active
curl "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"

# Expected response:
# {"ok":true,"result":{"url":"https://xxx.ngrok.io/webhook/telegram","has_custom_certificate":false,"pending_update_count":0}}
```

---

### **Issue 5: "Port 8000 already in use"**

**Cause:** Another process using the port

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000        # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or use different port
uvicorn main:app --port 8001
```

---

### **Issue 6: LLM returns generic/unhelpful answers**

**Cause:** Vector retrieval not finding relevant documents

**Solution:**
```bash
# 1. Check if documents were properly ingested
python -c "from src.services.rag_service import RAGService; r = RAGService(); docs = r.search('iuran BPJS', k=5); print(len(docs))"

# 2. Verify prompt in config/prompts.yaml is appropriate

# 3. Try increasing k (number of retrieved documents)
# In chat_service.py, line: docs = self.rag.search(query=query, k=5)  # Changed from k=3
```

---

### **Issue 7: "Connection refused" for Telegram API**

**Cause:** Network/firewall issue or invalid bot token

**Solution:**
```bash
# 1. Verify bot token is correct
echo $TELEGRAM_BOT_TOKEN

# 2. Test Telegram API connectivity
curl "https://api.telegram.org/bot<YOUR_TOKEN>/getMe"

# 3. Check if ngrok tunnel is active
# Should see: https://xxx.ngrok.io -> http://localhost:8000

# 4. Verify FastAPI server is running
# Should see: "Application startup complete"
```

---

## Development Tips

### **Local Testing Without Telegram**

```python
# In src/services/chat_service.py (main block)
if __name__ == "__main__":
    chat_service = ChatService()
    query = "Berapa iuran BPJS PBPU?"
    response = chat_service.generate_response(query, "test-session")
    print(f"Answer: {response.answer}")
    print(f"Sources: {response.sources}")
```

### **Adding More Documents**

```bash
# 1. Place PDF in data/raw_docs/
# 2. Re-run ingestion (it appends to existing DB)
python -m src.services.ingestion_service
# 3. No need to restart FastAPI servers
```

### **Viewing Vector DB Contents**

```python
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.core.config import settings

db = Chroma(
    persist_directory=str(settings.CHROMA_PERSIST_DIR),
    embedding_function=GoogleGenerativeAIEmbeddings(api_key=settings.GOOGLE_API_KEY)
)

# List all documents
count = db._collection.count()
print(f"Total documents: {count}")

# Search example
results = db.similarity_search("BPJS iuran", k=5)
for doc in results:
    print(f"Source: {doc.metadata.get('source')}")
    print(f"Content: {doc.page_content[:100]}...")
```

### **Debugging LLM Prompts**

Uncomment logging in `chat_service.py`:

```python
# Line ~45
self.logger.debug(f"system_instruction: {self.system_instruction}")

# Line ~60
self.logger.debug(f"Final prompt: {messages}")

# Line ~65
self.logger.debug(f"LLM response: {response}")
```

---

## Performance Optimization Tips

1. **Increase Chunk Size** (`ingestion_service.py`)
   - Larger chunks = faster retrieval but less granular
   - Current: 1000 chars (good balance)

2. **Adjust Temperature** (`chat_service.py`)
   - Current: 0.3 (factual)
   - Lower = more consistent, Higher = more creative

3. **Limit Retrieved Documents** (`chat_service.py`)
   - Current: k=3 (fast)
   - Increase k for more context (slower)

4. **Cache Session History**
   - Currently stored in memory (lost on restart)
   - Consider Redis/database for persistence

---

## Next Steps & Enhancements

- [ ] Add database persistence for chat history
- [ ] Implement user authentication
- [ ] Add analytics/monitoring dashboard
- [ ] Support for document uploads via Telegram
- [ ] Multi-language support
- [ ] Document QA with source highlighting
- [ ] Admin panel for document management
- [ ] Rate limiting & abuse prevention

---

## Support & Contributing

For issues, questions, or contributions:
1. Check [Troubleshooting](#troubleshooting) section
2. Review code comments in source files
3. Test in isolation using provided examples
4. Submit issues with:
   - Error message (full stack trace)
   - Steps to reproduce
   - Environment (Python version, OS)

---

## License

[Your License Here - e.g., MIT, Apache 2.0]

---

**Last Updated:** [Current Date]
**Maintainer:** [Your Name]
**Status:** ✅ Production Ready
