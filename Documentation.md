# 📚 Project Documentation
## AI QUERY API — Technical Assignment

> **Assignment:** AI/Full-Stack Developer Internship — Offshorly
> **Stack:** Python · FastAPI · Anthropic Claude · Pydantic · Uvicorn

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [Development Workflow](#3-development-workflow)
4. [Project File Structure](#4-project-file-structure)

---

---

# 1. Project Overview

## 1.1 Purpose

The **AI QUERY API** is a backend web service designed to demonstrate practical Artificial Intelligence integration within a clean, production-style REST API. It exposes two HTTP endpoints:

- **`GET /health`** — A diagnostic endpoint that confirms the application is running and that all required environment configuration is in place.
- **`POST /query`** — A general-purpose AI endpoint that accepts a natural language query from the user, processes it through a prompt engineering layer, sends it to a Large Language Model (LLM) API, and returns the model's response as a structured JSON object.

The application is intentionally kept simple in infrastructure (a single Python package, no database) so that the focus remains squarely on **AI/LLM integration quality and code organisation**.

---

## 1.2 Problem It Solves

Modern AI-powered applications need a reliable backend layer that can:

1. **Receive** arbitrary natural language input from a user or a frontend client.
2. **Interpret** the intent behind that input and select the right prompt strategy.
3. **Delegate** the enriched prompt to a capable LLM in a consistent and maintainable way.
4. **Return** the result in a predictable, structured format that a frontend or other service can safely consume.

Without a well-structured backend layer, LLM integrations tend to become tangled — with raw API calls scattered across the codebase, no separation between routing logic and AI logic, and no consistent error handling.

This project solves that by providing a **layered architecture** that clearly separates concerns: HTTP routing, request validation, prompt construction, LLM communication, and response formatting each live in their own dedicated layer.

---

## 1.3 AI/LLM Features Demonstrated

The following AI/LLM concepts are demonstrated through the `POST /query` endpoint:

| Concept | What It Shows |
|---|---|
| **LLM API Integration** | Making authenticated requests to an external AI provider (Anthropic Claude), handling API responses, and surfacing errors gracefully. |
| **Prompt Engineering** | Writing structured system prompts that guide model behaviour — setting tone, output format, constraints, and task framing. |
| **Zero-Shot Classification** | Instructing the model to assign a label (e.g., Positive/Negative/Neutral) to text it has never seen before, with no training examples provided. |
| **Long Context Handling** | Passing large bodies of text (articles, documents) into the model's context window and requesting a structured summary or analysis. |
| **Information Extraction** | Directing the model to identify and isolate specific pieces of data (e.g., phone numbers, names, dates) embedded within unstructured text. |
| **Relative Date Conversion** | Asking the model to resolve relative time expressions ("next Monday", "in 3 weeks") into absolute calendar dates, anchored to a fixed reference date of May 1, 2025. |
| **Structured Outputs** | Using system prompt instructions to enforce a consistent response format (prefix labels, field names, structured breakdowns) so that responses are reliable and parseable by downstream consumers. |
| **Random Integer Generation** | Parsing user-supplied numeric bounds (which may arrive as strings or integers) and returning a randomly generated integer within those bounds — demonstrating input coercion and deterministic model instruction. |

---

---

# 2. System Architecture

## 2.1 Component Overview

The application is composed of five distinct layers, each with a single, clear responsibility.

```
┌────────────────────────────────────────────────────────────┐
│                        CLIENT                              │
│          (curl, Postman, Frontend App, etc.)               │
└───────────────────────────┬────────────────────────────────┘
                            │  HTTP Request
                            ▼
┌────────────────────────────────────────────────────────────┐
│                     API LAYER (FastAPI)                     │
│   routes/health.py          routes/query.py                │
│   • Receives HTTP requests  • Validates request body       │
│   • Returns HTTP responses  • Returns HTTP responses       │
└───────────────────────────┬────────────────────────────────┘
                            │  Validated query string
                            ▼
┌────────────────────────────────────────────────────────────┐
│              PROMPT ENGINEERING LAYER                       │
│                  prompts/task_router.py                     │
│   • Detects the task type from the query text              │
│   • Selects and assembles the correct system prompt        │
│   • Returns a (system_prompt, user_message) tuple          │
└───────────────────────────┬────────────────────────────────┘
                            │  (system_prompt, user_message)
                            ▼
┌────────────────────────────────────────────────────────────┐
│                    SERVICE LAYER                            │
│                services/llm_service.py                      │
│   • Receives the prompt tuple                              │
│   • Builds the API request payload                         │
│   • Calls the LLM provider's HTTP API                      │
│   • Extracts and returns the text response                 │
└───────────────────────────┬────────────────────────────────┘
                            │  API call (HTTPS)
                            ▼
┌────────────────────────────────────────────────────────────┐
│                  LLM PROVIDER LAYER                         │
│           Anthropic Claude (or OpenAI / Gemini / Groq)     │
│   • Processes the prompt                                    │
│   • Returns a text completion                              │
└───────────────────────────┬────────────────────────────────┘
                            │  Text response
                            ▼
┌────────────────────────────────────────────────────────────┐
│               ENVIRONMENT CONFIGURATION                     │
│                      config.py + .env                       │
│   • Loads API keys and settings from environment            │
│   • Validates presence of required variables               │
│   • Exposes typed settings to all other layers             │
└────────────────────────────────────────────────────────────┘
```

---

## 2.2 Layer Descriptions

### API Layer (`routes/`)

This is the entry point for all HTTP traffic. FastAPI handles incoming requests, validates input using Pydantic schemas, delegates to the appropriate service or prompt layer, and formats the outgoing HTTP response. **This layer has no AI logic** — it only knows how to receive a request, call a service, and return a response.

### Service Layer (`services/llm_service.py`)

The service layer owns the actual communication with the LLM provider. It accepts a `system_prompt` and a `user_message`, assembles the API request payload, authenticates using the API key from `config.py`, makes the HTTP call, and returns the raw text from the model's response. This layer is **provider-aware but not task-aware** — swapping providers means changing only this file.

### Prompt Engineering Layer (`prompts/task_router.py`)

This layer is the intelligence of the application. It inspects the user's query to detect which of the supported tasks is being requested (classification, extraction, date conversion, etc.) and returns a precisely constructed system prompt paired with the user's message. This layer is **task-aware but not provider-aware** — it does not know which LLM will execute the prompt.

### LLM Provider Layer

The external LLM API (Anthropic Claude by default). The application treats this as a black box — it sends a prompt and receives a text completion. The provider can be swapped by modifying only `services/llm_service.py` and updating the API key in `.env`.

### Environment Configuration (`config.py`, `.env`)

`config.py` uses `python-dotenv` to load `.env` at startup, validates that required variables are present, and exposes a typed `Settings` object that all other layers import. This ensures that missing configuration is caught immediately at startup rather than at the moment of an API call.

---

## 2.3 Request Flow: `POST /query`

The following describes the complete lifecycle of a user request from arrival to response.

```
Step 1 ── Client sends POST /query with JSON body: {"query": "Extract the phone number from: ..."}

Step 2 ── FastAPI (routes/query.py) receives the request.
           Pydantic validates that the body has a "query" field of type string.
           If validation fails → 422 Unprocessable Entity is returned immediately.

Step 3 ── The validated query string is passed to the prompt engineering layer
           (prompts/task_router.py).
           The router inspects the query text for keywords and patterns.
           It detects "extract" + "phone number" → selects the INFORMATION_EXTRACTION prompt.
           It returns a tuple: (system_prompt, user_message).

Step 4 ── The (system_prompt, user_message) tuple is passed to the service layer
           (services/llm_service.py).
           The service builds the Anthropic API request payload:
           {
             "model": "claude-3-5-haiku-20241022",
             "max_tokens": 1024,
             "system": <system_prompt>,
             "messages": [{"role": "user", "content": <user_message>}]
           }
           The service authenticates using ANTHROPIC_API_KEY from config.py.
           The service sends the request to https://api.anthropic.com/v1/messages.

Step 5 ── Anthropic Claude processes the prompt and returns a JSON response.
           The service extracts the text from response.content[0].text.

Step 6 ── The extracted text is returned up the call stack to the route handler.
           The route handler wraps it: {"message": "<llm response text>"}
           FastAPI serialises this to JSON and returns HTTP 200.

Step 7 ── Client receives: {"message": "Extracted phone number: (02) 8123-4567"}
```

---

## 2.4 Request Flow: `GET /health`

```
Step 1 ── Client sends GET /health

Step 2 ── FastAPI (routes/health.py) receives the request.

Step 3 ── The handler imports the Settings object from config.py.
           It checks each required environment variable:
           - Is ANTHROPIC_API_KEY set? → "set" or "missing"
           - Is APP_ENV set?            → "set" or "missing"

Step 4 ── If all variables are present → overall status is "ok"
           If any variable is missing  → overall status is "degraded"

Step 5 ── Response is returned:
           {
             "status": "ok",
             "app_env": "development",
             "checks": {
               "ANTHROPIC_API_KEY": "set",
               "APP_ENV": "set"
             }
           }
```

---

---

# 3. Development Workflow

## 3.1 Setting Up the Project

Follow these steps to get the project running on your local machine from scratch.

### Step 1 — Clone the repository

```bash
git clone https://github.com/your-username/ai-query-api.git
cd ai-query-api
```

### Step 2 — Ensure Python 3.11+ is installed

```bash
python --version
# Should output: Python 3.11.x or higher
```

If not installed, download it from [python.org](https://www.python.org/downloads/).

### Step 3 — Create and activate a virtual environment

A virtual environment keeps your project's dependencies isolated from other Python projects on your system.

```bash
# Create the virtual environment in a folder named "venv"
python -m venv venv

# Activate it (macOS / Linux)
source venv/bin/activate

# Activate it (Windows Command Prompt)
venv\Scripts\activate.bat

# Activate it (Windows PowerShell)
venv\Scripts\Activate.ps1
```

You will see `(venv)` prepended to your terminal prompt when the environment is active.

### Step 4 — Install dependencies

```bash
pip install -r requirements.txt
```

---

## 3.2 Configuring Environment Variables

### Step 1 — Copy the example file

```bash
cp .env.example .env
```

### Step 2 — Obtain your API key

1. Go to [console.anthropic.com](https://console.anthropic.com).
2. Create an account or sign in.
3. Navigate to **API Keys** and create a new key.
4. Copy the key — it starts with `sk-ant-`.

### Step 3 — Add the key to your `.env` file

Open `.env` in any text editor:

```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
APP_ENV=development
```

### Important Notes

- **Never commit `.env` to version control.** It is already in `.gitignore`. Committing API keys is a serious security risk.
- The `GET /health` endpoint will immediately tell you if any required variable is missing, so you can catch configuration errors before running queries.
- To switch to a different LLM provider (e.g., OpenAI), you would replace `ANTHROPIC_API_KEY` with `OPENAI_API_KEY` in both `.env.example` and `config.py`, and update `services/llm_service.py` accordingly.

---

## 3.3 Running the Backend Server

### Development (recommended for local work)

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

| Flag | Meaning |
|---|---|
| `main:app` | Load the `app` object from `main.py` |
| `--reload` | Auto-restart the server when code files change |
| `--host 0.0.0.0` | Accept connections from any network interface |
| `--port 8000` | Listen on port 8000 |

### Production

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

For production, remove `--reload` and increase `--workers` based on your server's CPU core count.

### Verify it is running

Open your browser and visit:

- **Swagger UI (interactive docs):** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **Health check:** `http://localhost:8000/health`

---

## 3.4 Testing the Endpoints

### Option A — Using curl (command line)

**Health check:**
```bash
curl -X GET http://localhost:8000/health
```

**Query — basic:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is machine learning?"}'
```

**Query — classification:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Classify this text as Positive, Negative, or Neutral: \"The food was cold and tasteless.\""}'
```

**Query — phone extraction:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Extract the phone number from: Call us at 0917-123-4567 for reservations."}'
```

**Query — date conversion:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Convert to absolute date (today is May 1, 2025): next Friday"}'
```

**Query — random integer:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Generate a random integer between 1 and 100"}'
```

### Option B — Using Swagger UI

1. Open `http://localhost:8000/docs` in your browser.
2. Click on the endpoint you want to test.
3. Click **Try it out**.
4. Fill in the request body.
5. Click **Execute**.

### Option C — Using Postman

1. Import a new request: `POST http://localhost:8000/query`
2. Set the **Body** type to `raw` → `JSON`.
3. Paste your JSON body and click **Send**.

---

## 3.5 Adding New Prompt Tasks / Features

The application is designed to make adding new AI tasks straightforward. Follow these steps:

### Step 1 — Define a new task keyword

Open `prompts/task_router.py` and add a new detection condition in the `detect_task()` function:

```python
# Example: detecting a "translate" task
if any(word in query_lower for word in ["translate", "translation", "in spanish", "in french"]):
    return "translation"
```

### Step 2 — Write the system prompt

Add a new entry in the `SYSTEM_PROMPTS` dictionary in `task_router.py`:

```python
SYSTEM_PROMPTS = {
    # ... existing prompts ...
    "translation": """You are a professional translator. 
    Translate the user's text to the target language they specify.
    Always respond with:
    - Target language: <language>
    - Translation: <translated text>
    Be precise and preserve the original tone.""",
}
```

### Step 3 — Test your new task

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Translate to Spanish: Good morning, how are you?"}'
```

### Step 4 — Document it

Add an example to `README.md` under the **Prompt Task Examples** section so other developers can discover and use the new feature.

> **Tip:** You do not need to touch the route or service layer at all. New tasks are purely an addition to the prompt engineering layer.

---

---

# 4. Project File Structure

## 4.1 Full Structure

```
ai-query-api/
│
├── main.py
├── config.py
├── requirements.txt
├── .env.example
├── .env                    ← (git-ignored, created by developer)
├── .gitignore
├── README.md
├── DOCUMENTATION.md
│
├── routes/
│   ├── __init__.py
│   ├── health.py
│   └── query.py
│
├── services/
│   ├── __init__.py
│   └── llm_service.py
│
├── schemas/
│   ├── __init__.py
│   ├── query.py
│   └── health.py
│
└── prompts/
    ├── __init__.py
    └── task_router.py
```

---

## 4.2 File and Folder Responsibilities

### Root-level files

---

#### `main.py`

**Responsibility:** The application entry point. Creates the FastAPI `app` instance, registers all routers, and adds any global middleware (e.g., CORS headers).

**What it contains:**
- `app = FastAPI(...)` initialisation with title and version metadata
- `app.include_router(health_router)` and `app.include_router(query_router)`
- Optional: startup event handler that calls `config.validate_settings()` to fail fast on missing env vars

**Example:**
```python
from fastapi import FastAPI
from routes.health import router as health_router
from routes.query import router as query_router

app = FastAPI(title="AI QUERY API", version="1.0.0")
app.include_router(health_router)
app.include_router(query_router)
```

---

#### `config.py`

**Responsibility:** Centralises all environment variable loading and validation. Every other module imports from here — no other file should call `os.getenv()` directly.

**What it contains:**
- A `Settings` Pydantic `BaseSettings` class that reads from `.env`
- A list of required variable names for the health check
- A `validate_settings()` function for startup validation

**Example:**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ANTHROPIC_API_KEY: str
    APP_ENV: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()
REQUIRED_VARS = ["ANTHROPIC_API_KEY", "APP_ENV"]
```

---

#### `requirements.txt`

**Responsibility:** Declares all Python package dependencies with pinned or minimum versions. This ensures that anyone who clones the project installs the exact same packages.

**Contents:**
```
fastapi>=0.111.0
uvicorn[standard]>=0.29.0
pydantic>=2.7.0
pydantic-settings>=2.2.0
anthropic>=0.25.0
python-dotenv>=1.0.0
httpx>=0.27.0
```

---

#### `.env.example`

**Responsibility:** A committed, safe template of the `.env` file. It lists every required environment variable with placeholder values so that a new developer knows exactly what to configure. It contains **no real secrets**.

**Contents:**
```env
# Anthropic Claude API key — get one at https://console.anthropic.com
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Application environment
APP_ENV=development
```

---

#### `README.md`

**Responsibility:** The project's front page. Contains everything a developer needs to understand, install, run, and use the application. Written for a technical audience but accessible to beginners.

---

### `routes/` — API Layer

---

#### `routes/__init__.py`

**Responsibility:** Makes the `routes` directory a Python package. Typically empty.

---

#### `routes/health.py`

**Responsibility:** Defines the `GET /health` endpoint. Checks the application status and environment variable presence. Returns a structured `HealthResponse`.

**What it contains:**
- `router = APIRouter()` instance
- `@router.get("/health")` decorated handler function
- Logic to iterate over `REQUIRED_VARS` and check if each is set in the environment

**Example:**
```python
from fastapi import APIRouter
from schemas.health import HealthResponse
from config import settings, REQUIRED_VARS
import os

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def health_check():
    checks = {var: "set" if os.getenv(var) else "missing" for var in REQUIRED_VARS}
    status = "ok" if all(v == "set" for v in checks.values()) else "degraded"
    return HealthResponse(status=status, app_env=settings.APP_ENV, checks=checks)
```

---

#### `routes/query.py`

**Responsibility:** Defines the `POST /query` endpoint. Validates the request body, calls the prompt layer, calls the service layer, and returns the LLM's response.

**What it contains:**
- `router = APIRouter()` instance
- `@router.post("/query")` decorated handler function
- Dependency on `QueryRequest` schema (input validation) and `QueryResponse` schema (output formatting)
- Calls `task_router.build_prompt(query)` then `llm_service.call_llm(system_prompt, user_message)`

---

### `services/` — Service Layer

---

#### `services/llm_service.py`

**Responsibility:** Owns all communication with the LLM provider API. This is the only file that knows which LLM provider is being used and how to talk to it.

**What it contains:**
- An `anthropic.Anthropic` client instantiation using the key from `config.py`
- A `call_llm(system_prompt: str, user_message: str) -> str` function
- Model name constant (e.g., `MODEL = "claude-3-5-haiku-20241022"`)
- Error handling for API failures (connection errors, auth errors, rate limits)

**Example:**
```python
import anthropic
from config import settings

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
MODEL = "claude-3-5-haiku-20241022"

def call_llm(system_prompt: str, user_message: str) -> str:
    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}]
    )
    return message.content[0].text
```

---

### `schemas/` — Data Validation Layer

---

#### `schemas/query.py`

**Responsibility:** Defines the Pydantic models for the `POST /query` request body and response body. FastAPI uses these automatically for validation and serialisation.

**What it contains:**
```python
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    message: str
```

---

#### `schemas/health.py`

**Responsibility:** Defines the Pydantic model for the `GET /health` response body.

**What it contains:**
```python
from pydantic import BaseModel
from typing import Dict

class HealthResponse(BaseModel):
    status: str
    app_env: str
    checks: Dict[str, str]
```

---

### `prompts/` — Prompt Engineering Layer

---

#### `prompts/task_router.py`

**Responsibility:** The most AI-specific file in the project. Detects the user's intended task from their query text, selects the appropriate system prompt from the `SYSTEM_PROMPTS` dictionary, and returns both the system prompt and the user message to the caller.

**What it contains:**

1. **`SYSTEM_PROMPTS` dictionary** — A collection of carefully written system prompts, one per supported task. Each prompt gives the model a persona, output format instructions, and any task-specific constraints.

2. **`detect_task(query: str) -> str` function** — A simple keyword-based intent classifier that reads the query and returns a task name string (e.g., `"classification"`, `"extraction"`, `"date_conversion"`). Falls back to `"general"` if no specific task is detected.

3. **`build_prompt(query: str) -> tuple[str, str]` function** — Calls `detect_task()`, looks up the system prompt, and returns the `(system_prompt, user_message)` tuple.

**Supported task keys:**

| Key | Triggered by |
|---|---|
| `"classification"` | Keywords: `classify`, `category`, `sentiment`, `label` |
| `"extraction"` | Keywords: `extract`, `find`, `phone number`, `email`, `get the` |
| `"date_conversion"` | Keywords: `convert`, `date`, `when is`, `days from`, `next`, `last` |
| `"random_integer"` | Keywords: `random`, `integer`, `number between`, `generate a number` |
| `"long_context"` | Keywords: `summarize`, `summarise`, `key points`, `tldr`, `article` |
| `"general"` | Default fallback |

---

## 4.3 File Interaction Diagram

```
main.py
  └── imports → routes/health.py    → schemas/health.py
                                    → config.py
  └── imports → routes/query.py     → schemas/query.py
                                    → prompts/task_router.py
                                    → services/llm_service.py → config.py
                                                              → [Anthropic API]
```

All configuration flows from `config.py` outward. No layer directly reads environment variables — they always go through `config.py`.

---

## 4.4 Suggested `requirements.txt`

```
fastapi>=0.111.0
uvicorn[standard]>=0.29.0
pydantic>=2.7.0
pydantic-settings>=2.2.0
anthropic>=0.25.0
python-dotenv>=1.0.0
httpx>=0.27.0
```

## 4.5 Suggested `.gitignore`

```
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
env/
.env

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
```

---

*End of Documentation — AI Query API*