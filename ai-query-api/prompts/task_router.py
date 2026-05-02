# This is the prompt engineering layer.
# It detects the user's intent and returns the right system prompt.
#
# This is the most AI-specific file in the project.
# All the "prompt engineering" happens here — no AI logic in routes or services.

from datetime import datetime, timedelta
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