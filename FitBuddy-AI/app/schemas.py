from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from database import (
    get_original_plan,
    get_user,
    save_plan,
    save_user,
    update_plan,
)
from gemini_flash_generate import generate_nutrition_tip_with_flash
from gemini_generate import generate_workout_gemini
from updated_plan import update_workout_plan

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# Pydantic models for request validation
class UserInput(BaseModel):
    username: str
    user_id: int
    age: int
    weight: float
    goal: str
    intensity: str


class FeedbackRequest(BaseModel):
    user_id: int
    feedback: str


# 1. /generate-workout route
@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: int = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
):
    # Validate structure using Pydantic
    data = UserInput(
        username=username,
        user_id=user_id,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity,
    )

    # Save user details to database
    save_user(
        user_id=data.user_id,
        name=data.username,
        age=data.age,
        weight=data.weight,
        goal=data.goal,
        intensity=data.intensity,
    )

    # Call Gemini Pro for workout plan and Gemini Flash for nutrition tip
    workout_plan = generate_workout_gemini(data.model_dump())
    nutrition_tip = generate_nutrition_tip_with_flash(data.goal)

    # Store initial plan in database
    save_plan(user_id=data.user_id, plan=workout_plan)

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "user_id": data.user_id,
            "username": data.username,
            "workout_plan": workout_plan,
            "nutrition_tip": nutrition_tip,
        },
    )


# 2. /submit-feedback route
@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: int = Form(...),
    feedback: str = Form(...),
):
    # Validate structure using Pydantic
    fb_data = FeedbackRequest(user_id=user_id, feedback=feedback)

    # Retrieve existing plan from database
    original_plan = get_original_plan(fb_data.user_id)
    user = get_user(fb_data.user_id)

    if not original_plan:
        return HTMLResponse(content="Plan not found", status_code=404)

    # Send original + feedback to update_workout_plan (Gemini 1.5 Pro)
    revised_plan = update_workout_plan(original_plan, fb_data.feedback)

    # Update database record
    update_plan(user_id=fb_data.user_id, updated_text=revised_plan)

    nutrition_tip = generate_nutrition_tip_with_flash(
        user.goal if user else "fitness"
    )

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "user_id": fb_data.user_id,
            "username": user.name if user else "User",
            "workout_plan": revised_plan,
            "nutrition_tip": nutrition_tip,
        },
    )