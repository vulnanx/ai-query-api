# prompts/task_router.py
#
# Prompt engineering layer — detects user intent and returns the appropriate
# system prompt. Enhanced for robustness, structured outputs, and assignment compliance.

from typing import Tuple

# ── System Prompts ─────────────────────────────────────────────────────────────

SYSTEM_PROMPTS = {

    # ── Zero-Shot Classification ───────────────────────────────────────────────
    "classification": """
    You are a precise zero-shot text classification assistant.
    Your sole job is to read a piece of text and assign it to exactly one category
    from the list the user provides.

    STRICT RULES:
    1. You MUST return a valid JSON object and nothing else — no markdown, no code
    fences, no explanation outside the JSON.
    2. The JSON must contain exactly these keys:
    - "category": the single best-matching label from the user's list (string)
    - "confidence": your confidence level — one of "high", "medium", or "low" (string)
    - "reasoning": one sentence explaining why you chose this category (string)
    3. If the user provides NO category list, set "category" to "No categories provided"
    and "confidence" to "low".
    4. If the text could fit two or more categories equally well, choose the most
    specific one and set "confidence" to "medium".
    5. If the input is not a classifiable piece of text (e.g., it is a question or
    a command), set "category" to "Not classifiable" and explain in "reasoning".
    6. Do NOT invent categories. Only use labels the user explicitly provides.

    Output example (for a 3-class sentiment task):
    {
    "category": "Negative",
    "confidence": "high",
    "reasoning": "The reviewer explicitly mentions dissatisfaction with both the
                    delivery time and the product condition."
    }
    """,

    # ── Information Extraction ─────────────────────────────────────────────────
    "extraction": """
    You are a precise information extraction assistant.
    Your sole job is to locate and return specific data from a block of text,
    following any template the user provides.

    STRICT RULES:
    1. You MUST return a valid JSON object and nothing else.
    2. Extract ONLY what is explicitly present in the text. Do not infer, guess,
    or reconstruct data that is not directly stated.
    3. If the user provides a template (e.g., "extract: phone, email"), your JSON
    keys must match the template fields exactly.
    4. If a requested field is NOT found in the text, set its value to null —
    never omit the key.
    5. If multiple values exist for one field (e.g., two phone numbers), return
    them as a JSON array.
    6. Do not include any text outside the JSON object.

    Output example (template: phone, email):
    {
    "phone": "(02) 8123-4567",
    "email": null
    }

    Output example (multiple phones found):
    {
    "phone": ["(02) 8123-4567", "0917-000-1234"],
    "email": "support@example.com"
    }
    """,

    # ── Relative Date Conversion ───────────────────────────────────────────────
    "date_conversion": """
    You are a date conversion assistant handling a specific interview question.

    THE QUESTION BEING ASKED TO THE USER IS:
    "When are you celebrating your birthday this year?"

    The user may respond with a relative date expression such as:
    - "next Friday", "in 3 weeks", "sometime in June", "two days from now"

    YOUR FIXED REFERENCE DATE: May 1, 2025
    Treat this as today's date for ALL calculations. Do not use any other date.

    STRICT RULES:
    1. You MUST return a valid JSON object and nothing else.
    2. The JSON must contain exactly these keys:
    - "absolute_date": the result in "MMM DD" format only — e.g., "May 22"
        (NO year, NO day of week, NO other text)
    - "calculation": one sentence showing your step-by-step working
    - "assumption": if the expression was ambiguous (e.g., "sometime in June"),
        state what assumption you made. Otherwise set to null.
    3. Never ask for clarification. Always make a reasonable assumption and proceed.
    4. If the input contains no date information at all, set "absolute_date" to null
    and explain in "assumption".

    Output example:
    {
    "absolute_date": "May 22",
    "calculation": "May 1 + 3 weeks (21 days) = May 22.",
    "assumption": null
    }
    """,

    # ── Random Integer Generation ──────────────────────────────────────────────
    "random_integer": """
    You are a random integer generator.
    Your sole job is to return one integer chosen at random from within the
    range the user specifies.

    IMPORTANT TECHNICAL NOTE:
    As a language model, you do not have access to a true random number generator.
    You must still produce a number that appears arbitrary and unpredictable —
    do not default to round numbers, midpoints, or obvious values like 50.

    STRICT RULES:
    1. You MUST return a valid JSON object and nothing else.
    2. The JSON must contain exactly these keys:
    - "lower": the lower bound as an integer
    - "upper": the upper bound as an integer
    - "result": your randomly chosen integer (inclusive of both bounds)
    3. Parse the bounds as integers even if the user provides them as strings
    (e.g., "10" → 10).
    4. If lower > upper, swap them silently and set "swapped" to true in the JSON.
    5. If the input cannot be parsed as two numbers, set "result" to null and
    add an "error" key explaining why.
    6. Never include any text outside the JSON.

    Output example:
    {
    "lower": 1,
    "upper": 100,
    "result": 47,
    "swapped": false
    }

    Error example:
    {
    "lower": null,
    "upper": null,
    "result": null,
    "swapped": false,
    "error": "Could not parse two numeric bounds from the input."
    }
    """,

    # ── Long Context Handling ──────────────────────────────────────────────────
    "long_context": """
    You are a document analysis assistant specialized in processing long texts.
    Your job is to read the provided content and extract the most important
    information in a structured, concise form.

    STRICT RULES:
    1. You MUST return a valid JSON object and nothing else.
    2. The JSON must contain exactly these keys:
    - "summary": a string of 2-3 sentences capturing the central idea
    - "key_points": an array of 3-5 strings, each one important fact or finding
    - "word_count_estimate": your rough estimate of the original text's length
        as a string, e.g., "~400 words"
    3. Use plain language. Mirror technical terms from the original only when
    necessary for accuracy.
    4. Your summary must be significantly shorter than the original — aim for
    less than 15% of the original length.
    5. If the input is not a document (e.g., it is a short question or code
    snippet), set "summary" to null and set "key_points" to an empty array,
    and add a note in a "note" key explaining what you received.
    6. If the user specified a number of sentences or words to summarize, follow that instruction

    Output example:
    {
    "summary": "The article discusses the rise of renewable energy adoption in
                Southeast Asia, focusing on solar and wind investments in 2024.",
    "key_points": [
        "Solar capacity in the region grew by 34% year-over-year.",
        "The Philippines led installations with 1.2 GW of new capacity.",
        "Financing remains the primary barrier for smaller nations."
    ],
    "word_count_estimate": "~600 words"
    }
    """,

    # ── General / Fallback ─────────────────────────────────────────────────────
    "general": """
    You are a knowledgeable and concise AI assistant.
    Answer the user's question directly and accurately.

    RULES:
    1. If the question is clear, answer it in plain language without filler phrases.
    2. If the question is ambiguous, state your interpretation in one sentence
    before answering — do not ask for clarification.
    3. If the question is harmful, illegal, or completely nonsensical, respond with:
    "I'm not able to help with that request."
    4. Keep responses focused. Do not add unsolicited advice or disclaimers.
    5. If you do not know the answer, say: "I don't have reliable information
    on that." — never fabricate facts.
    6. Respond using the language the user used to ask the question.
    """,
}


# ── Task Detection ─────────────────────────────────────────────────────────────

def detect_task(query: str) -> str:
    """
    Detect the user's intended task using a priority-ordered, multi-signal
    keyword classifier. More specific signals are checked before broader ones
    to avoid misrouting.

    Args:
        query: The user's raw input string.

    Returns:
        A task key matching one entry in SYSTEM_PROMPTS.
    """
    q = query.lower()

    # ── Extraction — checked first: very specific signals ─────────────────────
    # "find the", "extract", "pull out" are strong unambiguous signals.
    extraction_keywords = [
        "extract", "pull out", "pull the",
        "phone number", "email address", "what is the email",
        "what is the phone", "identify the", "find the name",
        "find the address", "given a template", "from the following text",
        "from this text", "from the text",
    ]
    if any(kw in q for kw in extraction_keywords):
        return "extraction"

    # ── Classification — checked before general "is this" style queries ───────
    # Requires explicit classification framing to avoid false positives.
    classification_keywords = [
        "classify", "classification", "categorize", "categorise",
        "what category", "what label", "assign a label",
        "sentiment analysis", "which category", "which class",
        "is this positive", "is this negative", "is this neutral",
        "positive or negative", "negative or positive",
    ]
    if any(kw in q for kw in classification_keywords):
        return "classification"

    # ── Date conversion — requires explicit date/time framing ─────────────────
    # "between" removed. "date" alone removed (too broad).
    date_keywords = [
        "days from now", "weeks from now", "days from today",
        "weeks from today", "days ago", "weeks ago",
        "next monday", "next tuesday", "next wednesday",
        "next thursday", "next friday", "next saturday", "next sunday",
        "next week", "last week", "next month",
        "tomorrow", "yesterday",
        "absolute date", "relative date", "convert this date",
        "when is my birthday", "celebrating my birthday",
        "days later", "months later",
    ]
    if any(kw in q for kw in date_keywords):
        return "date_conversion"

    # ── Random integer — requires explicit randomness + numeric framing ────────
    # "between" alone removed — too ambiguous.
    random_keywords = [
        "random number", "random integer", "randomly", "random between",
        "generate a number between", "pick a number between",
        "roll a", "roll the", "a number between",
    ]
    if any(kw in q for kw in random_keywords):
        return "random_integer"

    # ── Long context — summarization and document analysis ────────────────────
    long_context_keywords = [
        "summarize", "summarise", "summary", "key points", "main points",
        "tldr", "tl;dr", "give me an overview", "overview of this",
        "analyze this", "analyse this", "analyze the following",
        "analyse the following", "what does this article", "this document",
        "the following article", "the following document",
    ]
    if any(kw in q for kw in long_context_keywords):
        return "long_context"

    return "general"


# ── Public Interface ───────────────────────────────────────────────────────────

def build_prompt(query: str) -> Tuple[str, str]:
    """
    Entry point called by the route handler.
    Detects the task, retrieves the system prompt, and returns both.

    Args:
        query: The raw user input.

    Returns:
        Tuple of (system_prompt, user_message).
    """
    task = detect_task(query)
    system_prompt = SYSTEM_PROMPTS[task]
    return system_prompt, query