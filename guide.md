# 🧠 Step-by-Step Build Guide
## AI Query API — Offshorly Internship Project
### A Complete Beginner's Guide to Building a FastAPI + Google Gemini Backend

---

> **Who this guide is for:** Complete beginners in AI integration who know basic Python but have never connected to an LLM API before.
>
> **What you will build:** A FastAPI backend with two endpoints (`GET /health` and `POST /query`) that routes user queries through Google Gemini to perform AI-powered tasks.
>
> **How this guide works:** We go milestone by milestone. Each step tells you *what file to create*, *the exact code to write*, *what that code actually does*, and *how to verify it works before moving on*.

---

## 📋 Table of Contents

- [Before You Start — Concepts](#before-you-start--concepts)
- [Milestone 1 — Project Setup](#milestone-1--project-setup)
- [Milestone 2 — Health Endpoint](#milestone-2--health-endpoint)
- [Milestone 3 — Query Endpoint Without AI](#milestone-3--query-endpoint-without-ai)
- [Milestone 4 — Gemini API Integration](#milestone-4--gemini-api-integration)
- [Milestone 5 — Prompt Task Router](#milestone-5--prompt-task-router)
- [Milestone 6 — Structured Outputs and Examples](#milestone-6--structured-outputs-and-examples)
- [Milestone 7 — Final Testing and GitHub Submission](#milestone-7--final-testing-and-github-submission)

---

---

# Before You Start — Concepts

Read this section first. It explains the key ideas behind what you are building. You do not need to memorise these — just read them once so the code makes sense as you go.

---

## 🤖 What is an LLM API?

LLM stands for **Large Language Model**. It is a type of AI that has been trained on enormous amounts of text and can understand and generate human language.

**Examples:** Google Gemini, OpenAI GPT-4, Anthropic Claude.

An **LLM API** is a way for your program to send a message to one of these AIs and receive a response — just like texting someone, except the person on the other end is an AI running on Google's (or OpenAI's) servers.

Think of it like this:

```
Your backend  ──→  "What is the capital of France?"  ──→  Google Gemini
Your backend  ←──  "The capital of France is Paris."  ←──  Google Gemini
```

Your code does not do any AI itself. It just sends requests and reads responses, like a messenger between your user and the AI.

---

## 🧠 What is Prompt Engineering?

When you send a message to an AI, the way you phrase that message has a huge effect on the quality and format of the response.

**Prompt engineering** is the practice of carefully writing instructions to get the AI to do exactly what you want.

**Bad prompt:** `"classify this"`  
**Good prompt:** `"You are a sentiment classifier. Read the following text and respond with exactly one word: Positive, Negative, or Neutral. No explanation needed."`

The second prompt will give you a consistent, predictable answer that your code can actually work with.

---

## 📋 What is a System Prompt?

Most LLM APIs let you send two things:

1. **A system prompt** — Background instructions for the AI. The user does not see this. It sets the "personality" and "rules" for the AI.
2. **A user message** — The actual thing the user typed.

Think of the system prompt as a briefing you give an employee before they take a customer call:

> *"You work for our company. Be polite. Always respond in English. Never give medical advice."*

The employee (AI) then uses those instructions when they talk to the customer (user).

In Gemini's SDK, the system prompt is passed via `system_instruction`.

---

## 🏷️ What is Zero-Shot Classification?

"Zero-shot" means the AI classifies something **without being shown any examples first**.

Normally, machine learning models need hundreds of labelled examples to learn. With LLMs, you can just describe what you want:

> *"Classify this text as Positive, Negative, or Neutral."*

The model figures it out from its training — you never had to provide a single labelled example. That is zero-shot classification.

---

## 📐 What is Structured Output?

By default, an AI might respond conversationally:

> *"Sure! I think this review is probably positive, because the author seems happy..."*

That is hard for your code to work with. **Structured output** means you use prompt engineering to force the AI to respond in a consistent, predictable format:

> *"Category: Positive"*

Your code can then reliably read and parse that response every time.

---

## 🔀 What Does Your Backend Do vs What Gemini Does?

| Your FastAPI Backend | Google Gemini |
|---|---|
| Receives the user's HTTP request | Processes the prompt and generates a response |
| Validates the request body | Does the actual AI thinking |
| Detects what task the user wants | Handles classification, extraction, dates, etc. |
| Builds the right prompt | Returns a text response |
| Sends the prompt to Gemini | Has no idea what your app looks like |
| Returns the response as JSON | Has no connection to your user directly |

Your backend is the **translator and coordinator**. Gemini is the **thinker**.

---

---

# Milestone 1 — Project Setup

**Goal:** Create the project folder, set up a virtual environment, install dependencies, and create the base file structure.

**When this milestone is done:** You will have a working Python environment and all the right files in place (even if most are empty).

---

## Step 1.1 — Create the project folder

Open your terminal and run:

```bash
mkdir ai-query-api
cd ai-query-api
```

**What this does:** Creates a new folder called `ai-query-api` and moves into it. This will be the root of your project.

---

## Step 1.2 — Create a virtual environment

```bash
python -m venv venv
```

Then activate it:

```bash
# macOS / Linux
source venv/bin/activate

# Windows Command Prompt
venv\Scripts\activate.bat

# Windows PowerShell
venv\Scripts\Activate.ps1
```

**What this does:** A virtual environment is an isolated Python installation just for this project. It means packages you install here won't affect other Python projects on your computer. You will see `(venv)` appear at the start of your terminal prompt when it is active.

**✅ Check:** Your terminal prompt should now start with `(venv)`.

---

## Step 1.3 — Create the folder structure

Run these commands one by one:

```bash
mkdir routes
mkdir services
mkdir schemas
mkdir prompts

touch main.py
touch config.py
touch requirements.txt
touch .env.example
touch .gitignore

touch routes/__init__.py
touch routes/health.py
touch routes/query.py

touch services/__init__.py
touch services/llm_service.py

touch schemas/__init__.py
touch schemas/health.py
touch schemas/query.py

touch prompts/__init__.py
touch prompts/task_router.py
```

> **Windows users:** Replace `touch` with `type nul >`, for example: `type nul > main.py`

**What this does:** Creates all the files and folders you will need. They are all empty for now — you will fill them in one milestone at a time.

**✅ Check:** Run `ls` (macOS/Linux) or `dir` (Windows). You should see `main.py`, `config.py`, `requirements.txt`, and four folders: `routes/`, `services/`, `schemas/`, `prompts/`.

---

## Step 1.4 — Create `requirements.txt`

Open `requirements.txt` and paste this:

```
fastapi>=0.111.0
uvicorn[standard]>=0.29.0
pydantic>=2.7.0
pydantic-settings>=2.2.0
google-genai>=1.0.0
python-dotenv>=1.0.0
```

**What each package does:**

| Package | What it does |
|---|---|
| `fastapi` | The web framework — handles HTTP requests and responses |
| `uvicorn` | The server — runs your FastAPI app so it can receive requests |
| `pydantic` | Validates data — makes sure request bodies have the right shape |
| `pydantic-settings` | Reads environment variables from your `.env` file safely |
| `google-genai` | The official Google SDK for talking to Gemini |
| `python-dotenv` | Loads your `.env` file into the environment at startup |

---

## Step 1.5 — Install dependencies

```bash
pip install -r requirements.txt
```

This will take a minute. It downloads all the packages listed in `requirements.txt`.

**✅ Check:** The command should finish without errors. You can also run `pip list` to see all installed packages.

---

## Step 1.6 — Create `.gitignore`

Open `.gitignore` and paste this:

```
# Virtual environment
venv/
env/

# Environment secrets — NEVER commit this
.env

# Python cache
__pycache__/
*.pyc
*.pyo

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
```

**What this does:** Tells Git to ignore these files and folders. The most important line is `.env` — your API key will live there, and you must never upload it to GitHub.

---

## Step 1.7 — Create `.env.example`

Open `.env.example` and paste this:

```env
# Copy this file to .env and fill in your values
# Get your Gemini API key at: https://aistudio.google.com/app/apikey

GEMINI_API_KEY=your-gemini-api-key-here
APP_ENV=development
```

**What this does:** This is a safe template that you *will* commit to GitHub. It shows other developers which environment variables they need to set up, without revealing any actual secrets.

---

## Step 1.8 — Create your actual `.env` file

```bash
cp .env.example .env
```

Then open `.env` and it will look like this:

```env
GEMINI_API_KEY=your-gemini-api-key-here
APP_ENV=development
```

Leave it as-is for now. You will add your real API key in Milestone 4.

**✅ Milestone 1 Complete** — Your project folder is set up with the right structure, dependencies are installed, and your environment files are in place. You are ready to write code.

---

---

# Milestone 2 — Health Endpoint

**Goal:** Build a working `GET /health` endpoint that checks if the app is running and if environment variables are set.

**When this milestone is done:** You can run the server and visit `http://localhost:8000/health` in your browser and see a JSON response.

**New concepts introduced:** FastAPI routers, Pydantic response models, environment variable loading.

---

## Step 2.1 — Create `config.py`

Open `config.py` and paste this:

```python
# config.py
# This file is responsible for loading and validating environment variables.
# Every other file in this project imports settings from here.
# No other file should ever call os.getenv() directly.

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Pydantic reads these fields automatically from your .env file.
    If a required field is missing, the app will crash immediately at startup
    with a clear error message — which is exactly what you want.
    """
    GEMINI_API_KEY: str        # Required — no default means it must be set
    APP_ENV: str = "development"  # Optional — defaults to "development"

    class Config:
        env_file = ".env"       # Tell Pydantic where to read variables from
        env_file_encoding = "utf-8"


# Create a single shared instance.
# Every other file does: from config import settings
settings = Settings()

# This list is used by the health endpoint to check each variable.
REQUIRED_VARS = ["GEMINI_API_KEY", "APP_ENV"]
```

**What this code does:**

- `BaseSettings` is a special Pydantic class that reads environment variables automatically.
- When Python imports this file, it immediately loads `.env` and tries to read `GEMINI_API_KEY`.
- If the variable is missing, the app crashes at startup with a clear message — much better than crashing in the middle of a user request.
- `REQUIRED_VARS` is a list we will loop over in the health endpoint to check whether each variable is present.

---

## Step 2.2 — Create `schemas/health.py`

Open `schemas/health.py` and paste this:

```python
# schemas/health.py
# This file defines the shape of the data our /health endpoint returns.
# Pydantic uses this to validate and serialize the response automatically.

from pydantic import BaseModel
from typing import Dict


class HealthResponse(BaseModel):
    """
    This is the exact JSON structure that GET /health will return.

    Example:
    {
        "status": "ok",
        "app_env": "development",
        "checks": {
            "GEMINI_API_KEY": "set",
            "APP_ENV": "set"
        }
    }
    """
    status: str           # "ok" or "degraded"
    app_env: str          # The value of APP_ENV from your .env file
    checks: Dict[str, str]  # Maps each variable name to "set" or "missing"
```

**What this does:** Defines the exact structure of the response JSON. FastAPI uses this to automatically validate and document the endpoint. If you return something that doesn't match this shape, FastAPI will catch the error.

---

## Step 2.3 — Create `routes/health.py`

Open `routes/health.py` and paste this:

```python
# routes/health.py
# This file defines the GET /health endpoint.
# It checks whether the app is running and whether required env vars are set.

import os
from fastapi import APIRouter
from schemas.health import HealthResponse
from config import settings, REQUIRED_VARS

# APIRouter is like a mini FastAPI app.
# We create one here, then attach it to the main app in main.py.
router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Checks if the app is running and all required environment variables are set.",
)
def health_check():
    """
    For each variable in REQUIRED_VARS, we check if it exists in the environment.
    If it does, we mark it as "set". If not, "missing".
    If all variables are set, the overall status is "ok". Otherwise, "degraded".
    """

    # Build a dictionary like: {"GEMINI_API_KEY": "set", "APP_ENV": "set"}
    checks = {}
    for var in REQUIRED_VARS:
        value = os.getenv(var)
        checks[var] = "set" if value else "missing"

    # Determine overall status
    all_set = all(status == "set" for status in checks.values())
    overall_status = "ok" if all_set else "degraded"

    return HealthResponse(
        status=overall_status,
        app_env=settings.APP_ENV,
        checks=checks,
    )
```

**What this does:**

- `@router.get("/health")` registers a function to handle `GET /health` requests.
- We loop over each required variable and check `os.getenv()` to see if it is present.
- We return a `HealthResponse` object — FastAPI converts it to JSON automatically.

---

## Step 2.4 — Create `main.py`

Open `main.py` and paste this:

```python
# main.py
# This is the entry point of the entire application.
# It creates the FastAPI app and connects all the routers.

from fastapi import FastAPI
from routes.health import router as health_router

# Create the FastAPI application instance.
# The title and description appear in the automatic Swagger UI docs.
app = FastAPI(
    title="AI Query API",
    description="A FastAPI backend that demonstrates LLM integration with Google Gemini.",
    version="1.0.0",
)

# Register the health router.
# This means FastAPI now knows about the GET /health endpoint.
app.include_router(health_router)


# Optional: a root endpoint so the API isn't blank at "/"
@app.get("/")
def root():
    return {"message": "AI Query API is running. Visit /docs for the interactive API explorer."}
```

**What this does:**

- `FastAPI()` creates the application.
- `app.include_router(health_router)` connects our health route to the app.
- The `@app.get("/")` gives us a friendly message at the root URL.

---

## Step 2.5 — Run the server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**What this command means:**
- `main` — look in `main.py`
- `app` — use the variable named `app` inside that file
- `--reload` — automatically restart the server when you save a file (great for development)
- `--port 8000` — listen on port 8000

**✅ Checks — do all three:**

**Check 1:** Open your browser and go to `http://localhost:8000/health`

You should see:
```json
{
  "status": "degraded",
  "app_env": "development",
  "checks": {
    "GEMINI_API_KEY": "missing",
    "APP_ENV": "set"
  }
}
```

`GEMINI_API_KEY` shows as "missing" because we haven't set it yet. That is fine for now — the endpoint is working correctly.

**Check 2:** Open `http://localhost:8000/docs`

You should see a Swagger UI page with your endpoints listed. This is auto-generated by FastAPI — you didn't have to write any documentation for it.

**Check 3:** Open `http://localhost:8000/`

You should see: `{"message": "AI Query API is running. Visit /docs for the interactive API explorer."}`

**✅ Milestone 2 Complete** — Your health endpoint is working. The app runs, the router is connected, and environment variables are being checked.

---

---

# Milestone 3 — Query Endpoint Without AI

**Goal:** Build the `POST /query` endpoint that accepts a JSON body and returns a response — but using a hardcoded placeholder instead of AI for now.

**When this milestone is done:** You can POST to `/query` and get back `{"message": "..."}`. The AI integration comes in Milestone 4.

**Why do this before the AI?** It is always good to build and test the HTTP layer first. If something breaks when you add Gemini, you will know the problem is in the AI layer, not the route or schema.

---

## Step 3.1 — Create `schemas/query.py`

Open `schemas/query.py` and paste this:

```python
# schemas/query.py
# Defines the shape of the request body and response body for POST /query.

from pydantic import BaseModel, field_validator


class QueryRequest(BaseModel):
    """
    This is what the user must send in the request body.

    Example request body:
    {
        "query": "What is machine learning?"
    }
    """
    query: str  # Must be a non-empty string

    @field_validator("query")
    @classmethod
    def query_must_not_be_empty(cls, value: str) -> str:
        """
        This validator runs automatically when a request comes in.
        If the query is empty or just whitespace, we reject it with a clear error.
        """
        if not value.strip():
            raise ValueError("Query cannot be empty or whitespace.")
        return value.strip()  # Remove leading/trailing spaces


class QueryResponse(BaseModel):
    """
    This is what our endpoint will return.

    Example response:
    {
        "message": "Machine learning is a type of AI..."
    }
    """
    message: str
```

**What this does:**

- `QueryRequest` validates that the request body has a `query` field that is a non-empty string.
- The `@field_validator` decorator adds a custom check — if someone sends `{"query": "   "}`, it returns a 422 error with a helpful message.
- `QueryResponse` defines the response shape: always a JSON object with a `message` key.

---

## Step 3.2 — Create `routes/query.py`

Open `routes/query.py` and paste this:

```python
# routes/query.py
# Defines the POST /query endpoint.
# Right now it returns a placeholder. We will connect Gemini in Milestone 4.

from fastapi import APIRouter, HTTPException
from schemas.query import QueryRequest, QueryResponse

router = APIRouter()


@router.post(
    "/query",
    response_model=QueryResponse,
    summary="Send a Query",
    description="Send a natural language query and receive an AI-generated response.",
)
def handle_query(request: QueryRequest):
    """
    Steps this endpoint will eventually do (fully implemented by Milestone 5):
    1. Receive and validate the user's query (done — Pydantic handles this)
    2. Detect the task type (e.g., classification, extraction)
    3. Build the right system prompt
    4. Send the prompt + query to Gemini
    5. Return the response as JSON

    For now, we return a placeholder so we can test the HTTP layer.
    """

    # PLACEHOLDER — will be replaced with actual AI logic in Milestone 4
    placeholder_response = (
        f"[Placeholder] You sent: '{request.query}'. "
        "AI integration coming in Milestone 4."
    )

    return QueryResponse(message=placeholder_response)
```

---

## Step 3.3 — Register the query router in `main.py`

Open `main.py` and add the query router:

```python
# main.py
from fastapi import FastAPI
from routes.health import router as health_router
from routes.query import router as query_router   # ← ADD THIS LINE

app = FastAPI(
    title="AI Query API",
    description="A FastAPI backend that demonstrates LLM integration with Google Gemini.",
    version="1.0.0",
)

app.include_router(health_router)
app.include_router(query_router)   # ← ADD THIS LINE


@app.get("/")
def root():
    return {"message": "AI Query API is running. Visit /docs for the interactive API explorer."}
```

Since you are running with `--reload`, the server will restart automatically when you save.

---

## Step 3.4 — Test the query endpoint

**Test 1 — Using curl:**

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is machine learning?"}'
```

Expected response:
```json
{
  "message": "[Placeholder] You sent: 'What is machine learning?'. AI integration coming in Milestone 4."
}
```

**Test 2 — Empty query (should be rejected):**

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": ""}'
```

Expected response (422 Validation Error):
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "query"],
      "msg": "Value error, Query cannot be empty or whitespace.",
      ...
    }
  ]
}
```

**Test 3 — Missing query field:**

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{}'
```

Expected: another 422 error saying `query` is required.

**Test 4 — Using Swagger UI:**

1. Go to `http://localhost:8000/docs`
2. Click `POST /query`
3. Click **Try it out**
4. In the body, type: `{"query": "Hello world"}`
5. Click **Execute**

**✅ Milestone 3 Complete** — The query endpoint exists, validates input, and returns a response. The HTTP layer is working perfectly. Time to connect the real AI.

---

---

# Milestone 4 — Gemini API Integration

**Goal:** Get a real Gemini API key, connect it to the service layer, and replace the placeholder with an actual AI response.

**When this milestone is done:** Sending a query to `POST /query` will return a real response generated by Google Gemini.

---

## Step 4.1 — Get your Gemini API key

1. Go to [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **Create API Key**
4. Copy the key — it starts with `AIza`

---

## Step 4.2 — Add the key to your `.env` file

Open `.env` and replace the placeholder:

```env
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
APP_ENV=development
```

Replace `AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` with your actual key.

> ⚠️ **Critical:** Never share this key. Never commit `.env` to GitHub. The `.gitignore` we created in Milestone 1 already prevents this — but double-check that `.env` is in your `.gitignore`.

---

## Step 4.3 — Verify the health endpoint reflects the key

Restart your server (stop with Ctrl+C, then run the uvicorn command again) and visit `http://localhost:8000/health`.

You should now see:
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

**✅ Check:** Status is `"ok"` and `GEMINI_API_KEY` is `"set"`.

---

## Step 4.4 — Create `services/llm_service.py`

This is the file that actually talks to Gemini. Open `services/llm_service.py` and paste this:

```python
# services/llm_service.py
# This file owns all communication with Google Gemini.
# It is the ONLY file in this project that knows we are using Gemini.
# If we ever switch to OpenAI or another provider, we only change this file.

from google import genai
from google.genai import types
from config import settings

# ── Model Configuration ────────────────────────────────────────────────────────
# gemini-2.0-flash is fast, capable, and cost-effective.
# You can change this to "gemini-1.5-pro" for higher quality responses.
MODEL = "gemini-2.0-flash"

# ── Client Initialization ──────────────────────────────────────────────────────
# We create the Gemini client once when this module loads.
# It uses your GEMINI_API_KEY from config.py automatically.
client = genai.Client(api_key=settings.GEMINI_API_KEY)


def call_llm(system_prompt: str, user_message: str) -> str:
    """
    Send a prompt to Google Gemini and return the text response.

    Args:
        system_prompt: Background instructions for the AI (the user doesn't see this).
                       Sets the AI's persona, response format, and task constraints.
        user_message:  The actual query from the user.

    Returns:
        The AI's response as a plain string.

    Raises:
        Exception: If the Gemini API call fails for any reason.
    """
    try:
        response = client.models.generate_content(
            model=MODEL,
            config=types.GenerateContentConfig(
                # system_instruction sets the AI's "rules" for this request
                system_instruction=system_prompt,

                # max_output_tokens limits how long the response can be
                # 1024 tokens is roughly 750 words — plenty for our tasks
                max_output_tokens=1024,

                # temperature controls creativity vs consistency
                # 0.2 = more consistent and predictable (good for structured tasks)
                # 1.0 = more creative and varied (good for open-ended questions)
                temperature=0.2,
            ),
            # contents is the user's actual message
            contents=user_message,
        )

        # response.text extracts the plain text from Gemini's response object
        return response.text

    except Exception as e:
        # Re-raise with a descriptive message so the route layer can handle it
        raise Exception(f"Gemini API call failed: {str(e)}")
```

**What this code does:**

- `genai.Client(api_key=...)` creates an authenticated connection to Google's Gemini servers.
- `client.models.generate_content(...)` sends your prompt and gets a response.
- `system_instruction` is the system prompt — the AI's "briefing" before it reads the user's message.
- `response.text` gives you just the text part of the response.
- The `try/except` block catches any API errors and re-raises them with a clear message.

---

## Step 4.5 — Update `routes/query.py` to use the LLM service

Open `routes/query.py` and replace the entire file content with this:

```python
# routes/query.py
# POST /query endpoint — now connected to Google Gemini.

from fastapi import APIRouter, HTTPException
from schemas.query import QueryRequest, QueryResponse
from services.llm_service import call_llm

router = APIRouter()

# A simple default system prompt.
# In Milestone 5, the prompt task router will replace this with task-specific prompts.
DEFAULT_SYSTEM_PROMPT = """
You are a helpful AI assistant integrated into a FastAPI backend application.
Answer the user's questions clearly, concisely, and accurately.
If the user asks you to perform a specific task like classification,
information extraction, or date conversion, do it precisely.
"""


@router.post(
    "/query",
    response_model=QueryResponse,
    summary="Send a Query",
    description="Send a natural language query and receive an AI-generated response.",
)
def handle_query(request: QueryRequest):
    """
    Receives the user's query, sends it to Gemini, and returns the response.
    """
    try:
        # Call Gemini with the default system prompt and the user's query
        ai_response = call_llm(
            system_prompt=DEFAULT_SYSTEM_PROMPT,
            user_message=request.query,
        )

        return QueryResponse(message=ai_response)

    except Exception as e:
        # If anything goes wrong with the Gemini call, return a 500 error
        raise HTTPException(
            status_code=500,
            detail=f"AI service error: {str(e)}",
        )
```

---

## Step 4.6 — Test the real AI integration

**Test 1 — Basic question:**

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is FastAPI in two sentences?"}'
```

Expected: A real AI-generated answer about FastAPI.

**Test 2 — From Swagger UI:**

1. Go to `http://localhost:8000/docs`
2. Click `POST /query` → **Try it out**
3. Enter: `{"query": "Explain machine learning in simple terms."}`
4. Click **Execute**
5. You should see a real Gemini response in the Response Body section.

**✅ Milestone 4 Complete** — Your backend now talks to Google Gemini. Real AI responses are flowing through your API.

---

---

# Milestone 5 — Prompt Task Router

**Goal:** Add a prompt engineering layer that detects what task the user wants and sends the right system prompt to Gemini.

**When this milestone is done:** The same `POST /query` endpoint will automatically handle classification, phone extraction, date conversion, random integers, long context, and general questions — using the appropriate prompt for each.

---

## Step 5.1 — Understand what the task router does

Right now, every query gets the same generic system prompt. That means if a user asks:

> *"Classify this as Positive, Negative, or Neutral: 'The food was cold.'"*

Gemini might respond conversationally:
> *"Sure! That seems like a negative sentiment to me, because..."*

With a task-specific prompt, Gemini would respond:
> *"Category: Negative"*

The task router inspects the user's query text, guesses what kind of task they want, and picks the right prompt.

---

## Step 5.2 — Create `prompts/task_router.py`

Open `prompts/task_router.py` and paste this:

```python
# prompts/task_router.py
# This is the prompt engineering layer.
# It detects the user's intent and returns the right system prompt.
#
# This is the most AI-specific file in the project.
# All the "prompt engineering" happens here — no AI logic in routes or services.

from typing import Tuple

# ── System Prompts Dictionary ──────────────────────────────────────────────────
# Each key is a task name. Each value is a carefully written system prompt.
# The quality of these prompts directly determines the quality of AI responses.

SYSTEM_PROMPTS = {

    # ── Zero-Shot Classification ───────────────────────────────────────────────
    "classification": """
You are a precise text classification assistant.
Your job is to read a piece of text and assign it to the correct category.
The user will specify the categories.

RULES:
- Always start your response with "Category: " followed by exactly one category label.
- Then on a new line, write "Reasoning: " followed by a brief one-sentence explanation.
- Do not write anything before "Category:".
- Do not add extra commentary or apologies.

Example output format:
Category: Positive
Reasoning: The reviewer praised both the service and the product quality.
""",

    # ── Information Extraction ─────────────────────────────────────────────────
    "extraction": """
You are a precise information extraction assistant.
Your job is to find and return specific pieces of information from text.

RULES:
- Extract only what is asked for. Do not guess or infer.
- If the information is found, start with a clear label followed by the value.
  Example: "Extracted phone number: (02) 8123-4567"
- If the information is NOT found in the text, respond with:
  "Not found: No [type of information] was found in the provided text."
- Do not include extra commentary.
""",

    # ── Relative Date Conversion ───────────────────────────────────────────────
    "date_conversion": """
You are a date calculation assistant.
Your job is to convert relative date expressions into absolute calendar dates.

IMPORTANT: Always treat today's date as May 1, 2025. This is fixed and must not change.

RULES:
- Always start with "Absolute date: " followed by the full date (e.g., "May 22, 2025").
- Then on a new line, write "Calculation: " followed by a brief explanation of how you arrived at the date.
- Use the format: Month Day, Year (e.g., May 22, 2025).
- Do not ask for clarification. Make a reasonable assumption and proceed.

Example output:
Absolute date: May 22, 2025
Calculation: Starting from May 1, 2025, adding 3 weeks (21 days) gives May 22, 2025.
""",

    # ── Random Integer Generation ──────────────────────────────────────────────
    "random_integer": """
You are a random number generator assistant.
Your job is to generate a single random integer within a user-specified range.

RULES:
- The user will provide two numbers as the lower and upper bounds.
- The numbers may be given as strings (e.g., "10") or integers (e.g., 10). Treat them as integers.
- Generate a random integer between the two bounds (inclusive).
- Respond with ONLY this format:
  "Random integer between [lower] and [upper]: [result]"
- Do not explain your process. Do not add extra text.

Example:
User: "Give me a random number between 1 and 100"
Response: Random integer between 1 and 100: 47
""",

    # ── Long Context Handling ──────────────────────────────────────────────────
    "long_context": """
You are a document summarization and analysis assistant.
Your job is to process long texts and extract the most important information.

RULES:
- Always structure your response with clear sections.
- Start with "Summary: " followed by 2-3 sentences capturing the main idea.
- Then write "Key Points:" followed by a numbered list of the most important facts.
- Use plain language. Avoid jargon unless it appears in the original text.
- Be concise — your summary should be much shorter than the original text.

Example output format:
Summary: [2-3 sentence overview of the main topic]

Key Points:
1. [Most important point]
2. [Second important point]
3. [Third important point]
""",

    # ── General / Fallback ─────────────────────────────────────────────────────
    "general": """
You are a helpful, knowledgeable AI assistant.
Answer the user's question clearly and concisely.
If the question is ambiguous, make a reasonable assumption and answer it.
Keep your response focused and avoid unnecessary filler.
""",
}


# ── Task Detection ─────────────────────────────────────────────────────────────

def detect_task(query: str) -> str:
    """
    Inspect the user's query and determine which task type it is.

    This is a simple keyword-based classifier. It checks for specific words
    and phrases that signal what the user wants to do.

    Args:
        query: The user's raw query string.

    Returns:
        A task name string that matches a key in SYSTEM_PROMPTS.
    """
    # Convert to lowercase so matching is case-insensitive
    q = query.lower()

    # ── Classification signals ─────────────────────────────────────────────────
    classification_keywords = [
        "classify", "classification", "categorize", "category",
        "sentiment", "label", "positive", "negative", "neutral",
        "is this", "what type", "what kind",
    ]
    if any(keyword in q for keyword in classification_keywords):
        return "classification"

    # ── Information extraction signals ────────────────────────────────────────
    extraction_keywords = [
        "extract", "find the", "get the", "pull out",
        "phone number", "email address", "phone", "email",
        "what is the number", "identify the",
    ]
    if any(keyword in q for keyword in extraction_keywords):
        return "extraction"

    # ── Date conversion signals ───────────────────────────────────────────────
    date_keywords = [
        "convert", "date", "when is", "days from", "weeks from",
        "next monday", "next friday", "next week", "last week",
        "tomorrow", "yesterday", "days ago", "days later",
        "absolute date", "relative date",
    ]
    if any(keyword in q for keyword in date_keywords):
        return "date_conversion"

    # ── Random integer signals ────────────────────────────────────────────────
    random_keywords = [
        "random", "randomly", "random number", "random integer",
        "generate a number", "pick a number", "between", "roll",
    ]
    if any(keyword in q for keyword in random_keywords):
        return "random_integer"

    # ── Long context / summarization signals ──────────────────────────────────
    long_context_keywords = [
        "summarize", "summarise", "summary", "key points", "tldr",
        "tl;dr", "main points", "overview", "article", "document",
        "long text", "analyze this text", "analyse this text",
    ]
    if any(keyword in q for keyword in long_context_keywords):
        return "long_context"

    # Default: return the general-purpose prompt
    return "general"


# ── Public Interface ───────────────────────────────────────────────────────────

def build_prompt(query: str) -> Tuple[str, str]:
    """
    The main function called by the route handler.

    Takes the user's raw query, detects the task, fetches the right system
    prompt, and returns both the system prompt and the user message as a tuple.

    Args:
        query: The user's raw query string.

    Returns:
        A tuple of (system_prompt, user_message).
        The route handler passes both to the LLM service.
    """
    task = detect_task(query)
    system_prompt = SYSTEM_PROMPTS[task]

    return system_prompt, query
```

**What this code does:**

- `SYSTEM_PROMPTS` is a dictionary of carefully written prompts, one per task. Think of each one as a different "mode" for the AI.
- `detect_task()` reads the user's query and returns which task it matches by looking for keywords.
- `build_prompt()` is the public function — it takes a query, detects the task, and returns the right prompt.
- The `Tuple[str, str]` return type means it returns two strings: the system prompt and the user message.

---

## Step 5.3 — Update `routes/query.py` to use the task router

Open `routes/query.py` and replace the entire file with this:

```python
# routes/query.py
# POST /query endpoint — now uses the prompt task router.

from fastapi import APIRouter, HTTPException
from schemas.query import QueryRequest, QueryResponse
from services.llm_service import call_llm
from prompts.task_router import build_prompt

router = APIRouter()


@router.post(
    "/query",
    response_model=QueryResponse,
    summary="Send a Query",
    description=(
        "Send a natural language query. The system automatically detects the task type "
        "(classification, extraction, date conversion, random integer, summarization, or general) "
        "and applies the appropriate prompt before calling Google Gemini."
    ),
)
def handle_query(request: QueryRequest):
    """
    Full request flow:
    1. Pydantic validates the request body (automatic).
    2. build_prompt() detects the task and selects the right system prompt.
    3. call_llm() sends the system prompt + user message to Gemini.
    4. The response is wrapped in QueryResponse and returned as JSON.
    """
    try:
        # Step 2: Get the right system prompt for this query
        system_prompt, user_message = build_prompt(request.query)

        # Step 3: Send to Gemini
        ai_response = call_llm(
            system_prompt=system_prompt,
            user_message=user_message,
        )

        # Step 4: Return the response
        return QueryResponse(message=ai_response)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI service error: {str(e)}",
        )
```

**What changed:** We replaced the hardcoded `DEFAULT_SYSTEM_PROMPT` with a call to `build_prompt(request.query)`, which dynamically selects the right prompt based on what the user typed.

---

## Step 5.4 — Test all task types

Run these tests one by one and verify each response is formatted correctly.

**Test 1 — Zero-Shot Classification:**

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Classify this review as Positive, Negative, or Neutral: The delivery was fast but the product was broken."}'
```

Expected format:
```
Category: Negative
Reasoning: ...
```

**Test 2 — Phone Number Extraction:**

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Extract the phone number from this text: Please call our support line at (02) 8123-4567 for assistance."}'
```

Expected format:
```
Extracted phone number: (02) 8123-4567
```

**Test 3 — Relative Date Conversion:**

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Convert this date: 3 weeks from today"}'
```

Expected format (anchored to May 1, 2025):
```
Absolute date: May 22, 2025
Calculation: ...
```

**Test 4 — Random Integer Generation:**

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Generate a random integer between 10 and 50"}'
```

Expected format:
```
Random integer between 10 and 50: [some number]
```

**Test 5 — Long Context (paste any long text):**

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Summarize this: Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by animals including humans. AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals."}'
```

Expected format:
```
Summary: ...

Key Points:
1. ...
2. ...
```

**✅ Milestone 5 Complete** — The prompt task router is working. Your single `/query` endpoint now handles six different AI tasks automatically, each with its own carefully crafted system prompt.

---

---

# Milestone 6 — Structured Outputs and Examples

**Goal:** Understand and demonstrate structured outputs, refine prompts if needed, and prepare curl and Swagger examples for the full feature set.

---

## Step 6.1 — What are structured outputs and why do they matter?

When your backend returns data that another program will read — a frontend, a mobile app, another API — that program needs to know exactly where to find each piece of information.

If Gemini responds:
> *"Well, based on my analysis, I'd say this is probably a positive review..."*

Your frontend cannot reliably extract the sentiment from that. But if it responds:
> *"Category: Positive"*

Your frontend can do `response.message.split(":")[1].trim()` and always get `"Positive"`.

**The system prompts in our task router enforce this structure** by giving the model strict formatting rules. This is prompt-based structured output — no special API mode needed.

---

## Step 6.2 — Optional: Add strict JSON output to a task

If you want a task to return actual JSON (machine-readable), you can instruct the model to do so in the prompt. Here is an example you can add to `SYSTEM_PROMPTS` in `task_router.py`:

```python
"extraction_json": """
You are an information extraction assistant.
Extract the requested information and return it ONLY as a valid JSON object.
Do not include any explanation, preamble, or markdown code fences.
Just return raw JSON.

Example output for phone number extraction:
{"field": "phone_number", "value": "(02) 8123-4567", "found": true}

Example output when not found:
{"field": "phone_number", "value": null, "found": false}
""",
```

> **Note:** For a beginner project, prompt-based structure (like `"Category: Positive"`) is completely acceptable and demonstrates structured output well. Strict JSON mode is a bonus enhancement.

---

## Step 6.3 — Full example request collection

Here is the complete set of working examples you can use in your submission and testing.

**Classification — Positive:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Classify this as Positive, Negative, or Neutral: I absolutely loved the service, the staff was friendly and the food was amazing!"}'
```

**Classification — Negative:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Classify this as Positive, Negative, or Neutral: The product stopped working after one day and customer support never responded."}'
```

**Phone Number Extraction:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Extract the phone number: For bookings, reach us at 0917-555-1234. Email us at info@example.com for other concerns."}'
```

**Date Conversion — Days:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Convert this date: 10 days from today"}'
```

**Date Conversion — Next weekday:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Convert this date: next Friday"}'
```

**Random Integer — String bounds:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Generate a random integer between '\''1'\'' and '\''100'\''"}'
```

**Random Integer — Integer bounds:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Pick a random number between 50 and 200"}'
```

**Long Context Summarization:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Summarize this article: [paste any paragraph of text here]"}'
```

**General Question:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the difference between supervised and unsupervised learning?"}'
```

---

## Step 6.4 — Test all examples in Swagger UI

1. Go to `http://localhost:8000/docs`
2. Click `POST /query` → **Try it out**
3. Run each example above by pasting the JSON body into the Request Body field
4. For each one, verify that the response format matches what the system prompt specifies

If a response doesn't look right, the fix is usually to improve the wording in the corresponding system prompt in `task_router.py`.

---

## Step 6.5 — Final check of your complete file structure

Run this in your terminal:

```bash
find . -not -path "./venv/*" -not -name "*.pyc" -not -path "./__pycache__/*"
```

You should see every file in the expected structure. Here is what it should look like:

```
.
├── .env
├── .env.example
├── .gitignore
├── config.py
├── main.py
├── requirements.txt
├── prompts/
│   ├── __init__.py
│   └── task_router.py
├── routes/
│   ├── __init__.py
│   ├── health.py
│   └── query.py
├── schemas/
│   ├── __init__.py
│   ├── health.py
│   └── query.py
└── services/
    ├── __init__.py
    └── llm_service.py
```

**✅ Milestone 6 Complete** — All six task types are working with structured outputs. You have a complete set of test examples.

---

---

# Milestone 7 — Final Testing and GitHub Submission

**Goal:** Do a full end-to-end test of everything, finalize your README, and push to GitHub.

---

## Step 7.1 — Full end-to-end test checklist

Run through every item below and confirm it works.

### Server
- [/] `uvicorn main:app --reload --host 0.0.0.0 --port 8000` starts without errors
- [/] `http://localhost:8000/` returns the welcome message
- [/] `http://localhost:8000/docs` loads the Swagger UI

### Health Endpoint
- [/] `GET /health` returns `"status": "ok"`
- [/] `GET /health` shows `"GEMINI_API_KEY": "set"`
- [/] `GET /health` shows `"APP_ENV": "set"`

### Query Endpoint — Input Validation
- [/] `POST /query` with `{"query": ""}` returns 422 with a clear error
- [/] `POST /query` with `{}` (missing field) returns 422
- [/] `POST /query` with `{"query": "   "}` (whitespace only) returns 422

### Query Endpoint — AI Tasks
- [/] Classification returns `"Category: ..."` format
- [/] Phone extraction returns `"Extracted phone number: ..."` format
- [/] Date conversion returns `"Absolute date: ..."` + `"Calculation: ..."` format
- [/] Random integer returns `"Random integer between X and Y: Z"` format
- [/] Summarization returns `"Summary: ..."` + `"Key Points: ..."` format
- [/] General questions return a clear, direct answer

---

## Step 7.2 — Prepare for GitHub

### Remove sensitive files

Make sure `.env` is **not** going to be committed:

```bash
git status
```

If `.env` appears in the output, something is wrong with your `.gitignore`. Fix it before proceeding.

### Initialize Git

```bash
git init
git add .
git commit -m "Initial commit: AI Query API with Gemini integration"
```

### Create a GitHub repository

1. Go to [github.com](https://github.com) and sign in
2. Click the **+** button → **New repository**
3. Name it `ai-query-api`
4. Set it to **Public**
5. Do **not** initialize with README (you already have one)
6. Click **Create repository**

### Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/ai-query-api.git
git branch -M main
git push -u origin main
```

---

## Step 7.3 — GitHub Submission Checklist

Go through every item below before submitting.

### Repository Structure
- [/] Repository is named `ai-query-api`
- [/] Repository is set to **Public**
- [/] `main.py` exists at the root
- [/] `config.py` exists at the root
- [/] `requirements.txt` exists at the root
- [/] `.env.example` exists and has `GEMINI_API_KEY` and `APP_ENV`
- [/] `.gitignore` exists and includes `.env`
- [/] `routes/health.py` exists
- [/] `routes/query.py` exists
- [/] `services/llm_service.py` exists
- [/] `schemas/health.py` and `schemas/query.py` exist
- [/] `prompts/task_router.py` exists

### Security
- [/] `.env` is **NOT** in the repository
- [/] No API keys are hardcoded anywhere in the source code
- [/] `GEMINI_API_KEY` only lives in `.env` (which is git-ignored)

### Functionality
- [/] `GET /health` works and returns correct JSON
- [/] `POST /query` works with all six task types
- [/] All task responses follow their structured output format
- [/] Invalid requests return 422 errors (not 500)
- [/] Swagger UI is accessible at `/docs`

### Code Quality
- [/] Every file has comments explaining what it does
- [/] No unused imports or variables
- [/] No hardcoded values that should be environment variables
- [/] All `__init__.py` files exist in every folder

### Documentation
- [/] `README.md` is present and polished
- [/] README includes installation instructions
- [/] README includes `.env` setup instructions
- [/] README includes how to run the server
- [/] README includes example curl requests for every task
- [/] README includes expected response formats

---

## Step 7.4 — Final project summary

Here is what you built and what each part demonstrates:

| File | What It Demonstrates |
|---|---|
| `main.py` | FastAPI app setup, router registration |
| `config.py` | Secure environment variable management with Pydantic |
| `routes/health.py` | Diagnostic endpoint, env var checking |
| `routes/query.py` | POST endpoint, input validation, error handling |
| `schemas/health.py` | Pydantic response model, data validation |
| `schemas/query.py` | Request validation, custom validators |
| `services/llm_service.py` | LLM API integration, service layer isolation |
| `prompts/task_router.py` | Prompt engineering, task routing, zero-shot classification, structured output, date conversion, information extraction, random generation |

| AI Concept | Where It Appears |
|---|---|
| LLM API integration | `services/llm_service.py` |
| Prompt engineering | `prompts/task_router.py` — every system prompt |
| System prompts | `SYSTEM_PROMPTS` dictionary |
| Zero-shot classification | `"classification"` prompt + test examples |
| Structured outputs | All prompt formatting rules |
| Information extraction | `"extraction"` prompt |
| Relative date conversion | `"date_conversion"` prompt (anchored to May 1, 2025) |
| Long context handling | `"long_context"` prompt |
| Random integer generation | `"random_integer"` prompt |

---

**🎉 Congratulations — you built a complete AI-powered FastAPI backend from scratch.**

You connected to a real LLM API, wrote effective system prompts, built a task routing layer, validated API inputs and outputs, and followed a clean, layered architecture.

---

*Built with FastAPI and Google Gemini — Offshorly AI/Full-Stack Developer Internship.*