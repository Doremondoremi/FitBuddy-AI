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
# GENERATE WORKOUT PLAN
# ==================================================

def generate_workout_plan(
    name: str,
    fitness_level: str,
    goal: str
) -> str:
    """
    Generate a structured 7-day workout plan.
    """

    prompt = f"""
Create a structured and beginner-friendly 7-day workout plan
for {name}.

Current fitness level: {fitness_level}
Primary goal: {goal}

For each day include:
- Warm-up
- Main workout
- Exercises with sets and reps
- Rest time
- Cool-down or recovery tip

Clearly format the plan from Day 1 to Day 7.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        if not response.text:
            return "Unable to generate workout plan."

        return response.text.strip()

    except Exception as e:
        return f"Error generating workout plan: {e}"


# ==================================================
# GENERATE NUTRITION TIPS
# ==================================================

def generate_nutrition_tips(
    fitness_level: str,
    goal: str
) -> str:
    """
    Generate concise nutrition and recovery tips.
    """

    prompt = f"""
Provide concise, practical nutrition and recovery tips
for someone with a fitness level of '{fitness_level}'
aiming to '{goal}'.

Keep the tips simple and easy to understand.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        if not response.text:
            return "Unable to generate nutrition tips."

        return response.text.strip()

    except Exception as e:
        return f"Error generating nutrition tips: {e}"


# ==================================================
# UPDATE WORKOUT PLAN
# ==================================================

def update_workout_plan(
    existing_plan: str,
    feedback: str
) -> str:
    """
    Update an existing workout plan based on user feedback.
    """

    prompt = f"""
Here is the existing 7-day workout plan:

{existing_plan}

The user provided this feedback:

"{feedback}"

Modify the workout plan according to the feedback.
Keep the 7-day structure clear and return the complete
updated workout plan.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        if not response.text:
            return "Unable to update workout plan."

        return response.text.strip()

    except Exception as e:
        return f"Error updating workout plan: {e}"