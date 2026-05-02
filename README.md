# 🤖 AI-Prompt-Engineering-API

> A full-stack AI application — FastAPI backend + Next.js chat frontend — demonstrating practical LLM capabilities through a clean, extensible REST API and a real-time chat interface. Built for the Offshorly AI/Full-Stack Developer Internship technical assignment.

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
- [Frontend — Chat UI](#-frontend--chat-ui)
- [API Documentation](#-api-documentation)
- [Example Requests & Responses](#-example-requests--responses)
- [Prompt Task Examples](#-prompt-task-examples)
- [Structured Outputs](#-structured-outputs)
- [Future Improvements](#-future-improvements)

---

## 📖 Description

**Offshorly LLM API Playground** is a full-stack AI application with two parts:

1. **FastAPI Backend** — A lightweight REST API that exposes `GET /health` and `POST /query` endpoints, routing natural language queries through a prompt engineering layer to **Google Gemini** (`gemini-2.0-flash`).

2. **Next.js Chat Frontend** — A real-time chat interface that lets users type messages, sends them to the FastAPI backend, and displays the full conversation history in a clean, responsive UI.

The project is designed to be a readable and extensible starting point for AI-powered full-stack development, showcasing foundational LLM techniques within a unified API and a production-quality frontend.

---

## ✨ Features

### Backend
| Feature | Description |
|---|---|
| 🏥 **Health Check** | Validates app status and required environment variable presence |
| 🔗 **LLM Integration** | Connects to Google Gemini (`gemini-2.0-flash`) via the `google-genai` SDK |
| 🧠 **Prompt Engineering** | Structured system prompts with task-specific instructions |
| 🏷️ **Zero-Shot Classification** | Categorizes text without any training examples |
| 📄 **Long Context Handling** | Processes and summarizes large text inputs |
| 🔍 **Information Extraction** | Extracts structured data (e.g., phone numbers) from free-form text |
| 📅 **Relative Date Conversion** | Converts relative dates (e.g., "next Monday") to absolute dates |
| 📐 **Structured Outputs** | Returns consistent, parseable LLM responses |
| 🎲 **Random Integer Generation** | Generates a random integer from two user-provided bounds |

### Frontend
| Feature | Description |
|---|---|
| 💬 **Real-Time Chat UI** | Message bubbles, role labels, and live conversation flow |
| 🗂️ **Conversation Memory** | Full message history stored in React state throughout the session |
| ⏳ **Loading Indicator** | Animated three-dot typing indicator while the AI responds |
| ⚠️ **Error Handling** | In-chat error messages when the backend is unreachable |
| ↩️ **Auto-Scroll** | Automatically scrolls to the latest message |
| 🧹 **Clear Chat** | One-click reset of the entire conversation |
| ⌨️ **Enter to Send** | Keyboard shortcut support alongside the Send button |

---

## 🛠️ Tech Stack

### Backend
- **Runtime**: Python 3.11+
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **ASGI Server**: [Uvicorn](https://www.uvicorn.org/)
- **LLM Provider**: [Google Gemini](https://deepmind.google/technologies/gemini/) (`gemini-2.0-flash`)
- **Gemini SDK**: [google-genai](https://pypi.org/project/google-genai/)
- **Validation**: [Pydantic v2](https://docs.pydantic.dev/)
- **Configuration**: [python-dotenv](https://pypi.org/project/python-dotenv/)

### Frontend
- **Framework**: [Next.js 14](https://nextjs.org/) (App Router)
- **UI Library**: [React 18](https://react.dev/)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **HTTP Client**: Native browser `fetch` API

---

## 📦 Requirements

- Python **3.11** or higher
- Node.js **18** or higher (`node --version` to check)
- `pip` and `npm` package managers
- A **Gemini API key** (free tier available at [aistudio.google.com](https://aistudio.google.com))
- Git (for cloning the repository)

---

## 🗂️ Project Structure

```
offshorly-llm-playground/
│
├── ai-query-api/                  # FastAPI backend
│   ├── main.py                    # FastAPI app entry point (includes CORS config)
│   ├── config.py                  # Environment variable loading & validation
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example               # Template for required environment variables
│   ├── .env                       # Your local secrets (git-ignored)
│   │
│   ├── routes/
│   │   ├── health.py              # GET /health endpoint
│   │   └── query.py               # POST /query endpoint
│   │
│   ├── services/
│   │   └── llm_service.py         # LLM API call logic
│   │
│   ├── schemas/
│   │   ├── query.py               # Request/response Pydantic models
│   │   └── health.py              # Health check response model
│   │
│   └── prompts/
│       └── task_router.py         # Detects task type and builds system prompts
│
└── ai-query-frontend/             # Next.js chat frontend
    ├── app/
    │   ├── layout.js              # Root layout wrapper
    │   ├── page.js                # Chat UI — main component
    │   └── globals.css            # Tailwind base styles
    ├── next.config.mjs
    ├── tailwind.config.mjs
    └── package.json
```

---

## ⚙️ Installation

### Backend

#### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-query-api.git
cd ai-query-api
```

#### 2. Create a Virtual Environment

```bash
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Frontend

#### 1. Navigate to the frontend folder

```bash
cd ai-query-frontend
```

#### 2. Install dependencies

```bash
npm install
```

> If you are setting up the frontend for the first time, scaffold it with:
> ```bash
> npx create-next-app@latest ai-query-frontend
> ```
> Choose: No TypeScript · Yes ESLint · Yes Tailwind CSS · No src/ dir · Yes App Router · No Turbopack · No import alias.

---

## 🔑 Environment Variables

Copy the example file and fill in your values:

```bash
cp .env.example .env
```

Then open `.env` and set your API key:

```env
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

Both the backend and frontend must run at the same time, in separate terminals.

### Terminal 1 — Backend

```bash
cd ai-query-api
source venv/bin/activate   # Windows: venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend available at: **`http://localhost:8000`**
Interactive API docs: **`http://localhost:8000/docs`**

### Terminal 2 — Frontend

```bash
cd ai-query-frontend
npm run dev
```

Chat UI available at: **`http://localhost:3000`**

---

## 💬 Frontend — Chat UI

The Next.js frontend lives in `ai-query-frontend/app/page.js` and is built with React hooks and Tailwind CSS.

### How it works

1. The user types a message and presses **Enter** or clicks **Send**
2. The message is added to the `messages` state array and displayed immediately in a blue bubble
3. A `fetch` POST request is sent to `http://localhost:8000/query` with the user's input
4. A three-dot loading indicator appears while the backend processes the request
5. The AI response is appended to `messages` and shown in a white bubble on the left
6. The page auto-scrolls to the latest message

### Key React concepts used

| Concept | Where it appears |
|---|---|
| `useState` | `messages`, `inputText`, `isLoading`, `errorText` |
| `useRef` | `messagesEndRef` — points to an invisible div at the bottom for auto-scrolling |
| `useEffect` | Triggers auto-scroll whenever `messages` changes |
| `async`/`await` | `sendMessage` function — waits for the backend response |
| Conditional rendering | Empty state, loading dots, error banner |

### CORS

The backend includes `CORSMiddleware` configured to allow requests from `http://localhost:3000`. This is required because the frontend (port 3000) and backend (port 8000) are different origins and browsers block cross-origin requests by default.

```python
# main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Conversation memory

Messages are stored as an array of `{ role, content }` objects in React state:

```js
[
  { role: "user",      content: "Classify this: Great product!" },
  { role: "assistant", content: "Category: Positive" },
]
```

This mirrors the standard conversation format used by OpenAI, Anthropic, and other LLM APIs, making it straightforward to extend the backend to accept full conversation history for multi-turn context.

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

Accepts a natural language query, routes it through the prompt engineering layer, calls Gemini, and returns the response.

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

```bash
curl -X GET http://localhost:8000/health
```

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

### Basic Question

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is FastAPI?"}'
```

```json
{
  "message": "FastAPI is a modern, high-performance Python web framework for building APIs. It is based on standard Python type hints and provides automatic interactive documentation, data validation via Pydantic, and async support out of the box."
}
```

---

## 🧪 Prompt Task Examples

The app automatically detects the user's intent and applies the appropriate system prompt.

---

### 🏷️ Zero-Shot Classification

```json
{
  "query": "Classify the following review — Positive, Negative, or Neutral: 'The delivery was late but the product worked perfectly.'"
}
```

```json
{
  "message": "Category: Neutral\n\nReasoning: The review contains both a negative element (late delivery) and a positive element (product worked perfectly), resulting in a mixed sentiment."
}
```

---

### 🔍 Information Extraction

```json
{
  "query": "Extract the phone number from: 'Please contact our support team at (02) 8123-4567 between 9am and 5pm.'"
}
```

```json
{
  "message": "Extracted phone number: (02) 8123-4567"
}
```

---

### 📅 Relative Date Conversion

```json
{
  "query": "Convert this relative date. Assume today is May 1, 2025: 'The deadline is in 3 weeks from today.'"
}
```

```json
{
  "message": "Absolute date: May 22, 2025\n\nCalculation: Starting from May 1, 2025, adding 3 weeks (21 days) gives May 22, 2025."
}
```

---

### 🎲 Random Integer Generation

```json
{
  "query": "Generate a random integer between '10' and '50'."
}
```

```json
{
  "message": "Random integer between 10 and 50: 37"
}
```

---

### 📄 Long Context Handling

```json
{
  "query": "Summarize the key points of the following article: [paste your text here]"
}
```

```json
{
  "message": "Key Points:\n1. ...\n2. ...\n3. ..."
}
```

---

## 📐 Structured Outputs

For tasks like extraction, classification, and date conversion, the system prompt instructs the LLM to return a **consistent, parseable format**:

- Classification results always begin with `Category:` followed by the label
- Extracted values are prefixed with a clear label (e.g., `Extracted phone number:`)
- Date conversions include both the result and the calculation breakdown
- Random numbers are returned as plain integers in the response message

These conventions make downstream parsing reliable without requiring strict JSON mode. If your use case requires machine-readable JSON directly, the service layer can be extended using Gemini's built-in structured output feature by setting `response_mime_type="application/json"` and passing a `response_schema` in the generation config.

---

## 🔮 Future Improvements

- [] **Conversation memory** — Session-level message history stored in React frontend state
- [ ] **Streaming responses** — Use Server-Sent Events (SSE) for real-time token streaming
- [ ] **Provider abstraction layer** — Hot-swap between Gemini, OpenAI, Anthropic, and Groq via a config flag
- [ ] **Multi-turn context** — Send full conversation history to the backend for context-aware responses
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

*Built using FastAPI, Google Gemini, Next.js, and React.*
