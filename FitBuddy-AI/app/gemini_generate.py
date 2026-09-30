def generate_workout_gemini(user_input: dict) -> str:

    name = user_input.get("name", "User")
    age = user_input.get("age", "")
    weight = user_input.get("weight", "")
    goal = user_input.get("goal", "General Fitness")
    intensity = user_input.get("intensity", "Moderate")

    plan = f"""
PERSONALIZED WORKOUT PLAN

Name: {name}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}


MONDAY - FULL BODY

• Bodyweight Squats - 3 sets × 10 reps
• Wall Push-ups - 3 sets × 10 reps
• Glute Bridges - 3 sets × 12 reps
• Easy Stretching - 5 minutes


TUESDAY - LIGHT CARDIO

• Brisk Walking - 20 minutes
• Marching in Place - 5 minutes
• Light Mobility - 10 minutes


WEDNESDAY - REST

• Rest and recovery
• Gentle stretching if comfortable


THURSDAY - FULL BODY

• Step-ups - 3 sets × 10 reps
• Incline Push-ups - 3 sets × 8 reps
• Bird Dog - 3 sets × 8 each side
• Cool-down stretching - 5 minutes


FRIDAY - CARDIO & MOBILITY

• Brisk Walk - 20 minutes
• Marching - 3 × 2 minutes
• Mobility exercises - 10 minutes


SATURDAY - LIGHT ACTIVITY

• Easy walking
• Stretching
• Relaxation


SUNDAY - REST

• Rest and recovery


IMPORTANT

Start comfortably and focus on proper technique.
Increase activity gradually.
Stop an exercise if it causes pain or feels unsafe.
"""

    return plan