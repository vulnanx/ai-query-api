# This file owns all communication with Google Gemini.
# It is the ONLY file in this project that knows we are using Gemini.
# If we ever switch to OpenAI or another provider, we only change this file.

from google import genai
from google.genai import types
from config import settings

# ── Model Configuration ────────────────────────────────────────────────────────
# gemini-2.0-flash is fast, capable, and cost-effective.
MODEL = "gemini-2.5-flash-lite"

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
        # sends your prompt and gets a response
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