# 🤖 Offshorly LLM API Playground

> A FastAPI backend that demonstrates practical LLM capabilities through a clean, extensible REST API — built for the Offshorly AI/Full-Stack Developer Internship technical assignment.

---

## 📋 Table of Contents

- [Description](#-description)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Requirements](#-requirements)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Environment Variables](#-environment-variables)
- [Running the App](#-running-the-app)
- [API Documentation](#-api-documentation)
- [Example Requests & Responses](#-example-requests--responses)
- [Prompt Task Examples](#-prompt-task-examples)
- [Structured Outputs](#-structured-outputs)
- [Future Improvements](#-future-improvements)

---

## 📖 Description

**Offshorly LLM API Playground** is a lightweight FastAPI application that exposes two REST endpoints — `GET /health` and `POST /query` — to demonstrate real-world LLM integration patterns. It routes natural language user queries through a prompt engineering layer before sending them to **Google Gemini**, Google's multimodal large language model API.

The application is designed to be a clean, readable, and extensible starting point for AI-powered backend development, showcasing several foundational LLM techniques within a single unified API.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🏥 **Health Check** | Validates app status and required environment variable presence |
| 🔗 **LLM Integration** | Connects to Google Gemini (`gemini-2.0-flash`) via the `google-genai` SDK |
| 🧠 **Prompt Engineering** | Structured system prompts with task-specific instructions |
| 🏷️ **Zero-Shot Classification** | Categorizes text without any training examples |
| 📄 **Long Context Handling** | Processes and summarizes large text inputs |
| 🔍 **Information Extraction** | Extracts structured data (e.g., phone numbers) from free-form text |
| 📅 **Relative Date Conversion** | Converts relative dates (e.g., "next Monday") to absolute dates, anchored to **May 1, 2025** |
| 📐 **Structured Outputs** | Returns JSON-formatted, schema-consistent LLM responses |
| 🎲 **Random Integer Generation** | Generates a random integer from two user-provided bounds (as strings or integers) |

---

## 🛠️ Tech Stack

- **Runtime**: Python 3.11+
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **ASGI Server**: [Uvicorn](https://www.uvicorn.org/)
- **LLM Provider**: [Google Gemini](https://deepmind.google/technologies/gemini/) (`gemini-2.0-flash`)
- **Gemini SDK**: [google-genai](https://pypi.org/project/google-genai/)
- **Validation**: [Pydantic v2](https://docs.pydantic.dev/)
- **Configuration**: [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## 📦 Requirements

- Python **3.11** or higher
- `pip` package manager
- A **Gemini API key** (free tier available at [aistudio.google.com](https://aistudio.google.com))
- Git (for cloning the repository)

---

## 🗂️ Project Structure

```
ai-query-api/
├── main.py                  # FastAPI app entry point
├── config.py                # Environment variable loading & validation
├── requirements.txt         # Python dependencies
├── .env.example             # Template for required environment variables
├── .env                     # Your local secrets (git-ignored)
├── README.md                # This file
│
├── routes/
│   ├── __init__.py
│   ├── health.py            # GET /health endpoint
│   └── query.py             # POST /query endpoint
│
├── services/
│   ├── __init__.py
│   └── llm_service.py       # LLM API call logic
│
├── schemas/
│   ├── __init__.py
│   ├── query.py             # Request/response Pydantic models
│   └── health.py            # Health check response model
│
└── prompts/
    ├── __init__.py
    └── task_router.py       # Detects task type and builds system prompts
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-query-api.git
cd ai-query-api
```

### 2. Create a Virtual Environment

```bash
# Create the virtual environment
python -m venv venv

# Activate it — macOS/Linux
source venv/bin/activate

# Activate it — Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Copy the example file and fill in your values:

```bash
cp .env.example .env
```

Then open `.env` and set your API key:

```env
# .env
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
APP_ENV=development
```

### Variable Reference

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | ✅ Yes | Your Gemini API key from [aistudio.google.com](https://aistudio.google.com/app/apikey) |
| `APP_ENV` | ✅ Yes | Application environment (`development` or `production`) |

> **Note:** Never commit your `.env` file. It is already listed in `.gitignore`.

---

## 🚀 Running the App

### Development Mode (with auto-reload)

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at: **`http://localhost:8000`**

Interactive docs (Swagger UI): **`http://localhost:8000/docs`**

ReDoc: **`http://localhost:8000/redoc`**

---

## 📡 API Documentation

### `GET /health`

Checks whether the application is running and whether all required environment variables are present.

**Response Schema**

```json
{
  "status": "ok" | "degraded",
  "app_env": "development",
  "checks": {
    "GEMINI_API_KEY": "set" | "missing",
    "APP_ENV": "set" | "missing"
  }
}
```

---

### `POST /query`

Accepts a natural language query, routes it through the prompt engineering layer, calls the LLM, and returns the response.

**Request Schema**

```json
{
  "query": "string"
}
```

**Response Schema**

```json
{
  "message": "string"
}
```

**Error Responses**

| Code | Meaning |
|---|---|
| `422` | Validation error — `query` field missing or not a string |
| `500` | LLM provider error or internal server error |

---

## 🔬 Example Requests & Responses

### Health Check

**Request**
```bash
curl -X GET http://localhost:8000/health
```

**Response**
```json
{
  "status": "ok",
  "app_env": "development",
  "checks": {
    "GEMINI_API_KEY": "set",
    "APP_ENV": "set"
  }
}
```

---

### POST /query — Basic Question

**Request**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is FastAPI?"}'
```

**Response**
```json
{
  "message": "FastAPI is a modern, high-performance Python web framework for building APIs. It is based on standard Python type hints and provides automatic interactive documentation, data validation via Pydantic, and async support out of the box."
}
```

---

## 🧪 Prompt Task Examples

The app automatically detects the user's intent and applies the appropriate system prompt. Below are examples of each supported task.

---

### 🏷️ Zero-Shot Classification

The model classifies text into a category without any labelled training examples.

**Request**
```json
{
  "query": "Classify the following review into one of these categories — Positive, Negative, or Neutral: 'The delivery was late and the packaging was damaged, but the product itself worked perfectly.'"
}
```

**Response**
```json
{
  "message": "Category: Neutral\n\nReasoning: The review contains both a negative element (late delivery, damaged packaging) and a positive element (product worked perfectly), resulting in a mixed sentiment that is best classified as Neutral."
}
```

---

### 🔍 Information Extraction

The model extracts structured data from unstructured text.

**Request**
```json
{
  "query": "Extract the phone number from this text: 'Please contact our support team at (02) 8123-4567 between 9am and 5pm, Monday to Friday. You can also reach us at support@example.com for non-urgent concerns.'"
}
```

**Response**
```json
{
  "message": "Extracted phone number: (02) 8123-4567"
}
```

---

### 📅 Relative Date Conversion

The model converts relative date expressions to absolute dates, assuming today is **May 1, 2025**.

**Request**
```json
{
  "query": "Convert this relative date to an absolute date. Assume today is May 1, 2025: 'The project deadline is in 3 weeks from today.'"
}
```

**Response**
```json
{
  "message": "Absolute date: May 22, 2025\n\nCalculation: Starting from May 1, 2025, adding 3 weeks (21 days) gives May 22, 2025."
}
```

---

### 🎲 Random Integer Generation

The model generates a random integer from two user-provided bounds. Both values can be passed as strings or integers.

**Request**
```json
{
  "query": "Generate a random integer between '10' and '50'."
}
```

**Response**
```json
{
  "message": "Random integer between 10 and 50: 37"
}
```

---

### 📄 Long Context Handling

Paste a long document and ask for a summary or analysis.

**Request**
```json
{
  "query": "Summarize the key points of the following article: [paste your long text here]"
}
```

**Response**
```json
{
  "message": "Key Points:\n1. ...\n2. ...\n3. ..."
}
```

---

## 📐 Structured Outputs

For tasks like extraction, classification, and date conversion, the system prompt instructs the LLM to return a **consistent, parseable format**. This means:

- Classification results always begin with `Category:` followed by the label.
- Extracted values are prefixed with a clear label (e.g., `Extracted phone number:`).
- Date conversions always include both the result and the calculation breakdown.
- Random numbers are always returned as plain integers in the response message.

These conventions make downstream parsing reliable without requiring strict JSON mode. If your use case requires machine-readable JSON output directly, the service layer can be extended to use Gemini's built-in structured output feature by setting `response_mime_type="application/json"` and passing a `response_schema` in the generation config.

---

## 🔮 Future Improvements

- [ ] **Streaming responses** — Use Server-Sent Events (SSE) for real-time token streaming
- [ ] **Provider abstraction layer** — Hot-swap between Gemini, OpenAI, Anthropic, and Groq via a config flag
- [ ] **Conversation history** — Maintain session context for multi-turn conversations
- [ ] **Strict JSON mode** — Return all structured tasks as validated JSON objects
- [ ] **Rate limiting** — Add per-IP rate limiting middleware using `slowapi`
- [ ] **Authentication** — Protect endpoints with API key auth headers
- [ ] **Logging & observability** — Integrate structured logging with request tracing
- [ ] **Docker support** — Add `Dockerfile` and `docker-compose.yml` for containerized deployment
- [ ] **Unit tests** — Add `pytest` test suite for routes, services, and prompt routing logic
- [ ] **Async LLM calls** — Upgrade service layer to fully async with `asyncio`

---

## 📄 License

This project was created for the **Offshorly AI/Full-Stack Developer Internship** technical assignment. Feel free to use it as a learning reference.

---

*Built with ❤️ using FastAPI and Google Gemini.*