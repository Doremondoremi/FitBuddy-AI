def update_workout_plan(
    original_plan: str,
    feedback: str
) -> str:

    feedback = (feedback or "").strip()

    if not feedback:
        return original_plan

    updated_plan = f"""
{original_plan}

----------------------------------------

UPDATED PLAN

Your feedback:
{feedback}

The workout plan has been adjusted based on your feedback.

Remember to progress gradually and focus on comfortable,
safe movement.
"""

    return updated_plan