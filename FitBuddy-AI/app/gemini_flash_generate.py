import os

from dotenv import load_dotenv
from google import genai


# ==================================================
# LOAD ENVIRONMENT VARIABLES
# ==================================================

load_dotenv()


# ==================================================
# GEMINI API CONFIGURATION
# ==================================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the .env file.")

client = genai.Client(api_key=api_key)


# ==================================================
# GENERATE NUTRITION TIP
# ==================================================

def generate_nutrition_tip_with_flash(goal: str) -> str:
    """
    Generate a short nutrition or recovery tip
    based on the user's fitness goal.
    """

    prompt = f"""
Give one clear, helpful nutrition or recovery tip
for someone focused on '{goal}'.

The tip should be:
- Short
- Practical
- Easy to understand
- Suitable for a general fitness user
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        if not response.text:
            return "Unable to generate nutrition tip."

        return response.text.strip()

    except Exception as e:
        return f"Error generating nutrition tip: {e}"