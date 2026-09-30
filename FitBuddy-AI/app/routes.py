from pathlib import Path

from fastapi import (
    APIRouter,
    Request,
    Form,
    HTTPException
)

from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates

from pydantic import BaseModel


# ==================================================
# DATABASE
# ==================================================

from database import (
    save_user,
    save_plan,
    update_plan as save_updated_plan,
    get_original_plan,
    get_user,
    get_all_users,
    get_all_plans,
)


# ==================================================
# AI
# ==================================================

from gemini_generate import generate_workout_gemini

from updated_plan import update_workout_plan


# ==================================================
# ROUTER
# ==================================================

router = APIRouter()


# ==================================================
# TEMPLATE LOCATION
# ==================================================

TEMPLATE_DIR = (
    Path(__file__).resolve().parent / "templates"
)

templates = Jinja2Templates(
    directory=str(TEMPLATE_DIR)
)


# ==================================================
# NUTRITION TIP
# ==================================================

def generate_nutrition_tip_with_flash(goal: str):

    return (
        f"For your {goal} goal, stay hydrated and include "
        "a balanced combination of vegetables, fruits, "
        "whole grains and protein-rich foods."
    )


# ==================================================
# API MODELS
# ==================================================

class UserInput(BaseModel):

    user_id: int
    username: str
    age: int
    weight: float
    goal: str
    intensity: str


class FeedbackRequest(BaseModel):

    feedback: str


class WorkoutRequest(BaseModel):

    goal: str
    intensity: str


# ==================================================
# HOME PAGE
# ==================================================

@router.get("/", response_class=HTMLResponse)
def index_view(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


# ==================================================
# GENERATE WORKOUT
# ==================================================

@router.post(
    "/generate-workout",
    response_class=HTMLResponse
)
def generate_workout(

    request: Request,

    username: str = Form(...),

    user_id: int = Form(...),

    age: int = Form(...),

    weight: float = Form(...),

    goal: str = Form(...),

    intensity: str = Form(...),
):

    # ----------------------------------------------
    # SAVE USER
    # ----------------------------------------------

    save_user(
        user_id=user_id,
        name=username,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity
    )


    # ----------------------------------------------
    # USER DATA
    # ----------------------------------------------

    user_input = {

        "user_id": user_id,

        "name": username,

        "age": age,

        "weight": weight,

        "goal": goal,

        "intensity": intensity
    }


    # ----------------------------------------------
    # GENERATE WORKOUT
    # ----------------------------------------------

    workout_plan = generate_workout_gemini(
        user_input
    )


    # ----------------------------------------------
    # NUTRITION TIP
    # ----------------------------------------------

    nutrition_tip = (
        generate_nutrition_tip_with_flash(goal)
    )


    # ----------------------------------------------
    # SAVE PLAN
    # ----------------------------------------------

    save_plan(
        user_id,
        workout_plan
    )


    # ----------------------------------------------
    # SHOW RESULT
    # ----------------------------------------------

    return templates.TemplateResponse(

        request=request,

        name="result.html",

        context={

            "request": request,

            "username": username,

            "user_id": user_id,

            "age": age,

            "weight": weight,

            "goal": goal,

            "intensity": intensity,

            "workout_plan": workout_plan,

            "nutrition_tip": nutrition_tip
        }
    )


# ==================================================
# SUBMIT FEEDBACK
# ==================================================

@router.post(
    "/submit-feedback",
    response_class=HTMLResponse
)
def submit_feedback(

    request: Request,

    user_id: int = Form(...),

    feedback: str = Form(...)
):

    # ----------------------------------------------
    # GET ORIGINAL PLAN
    # ----------------------------------------------

    original_plan = get_original_plan(
        user_id
    )


    # ----------------------------------------------
    # GET USER
    # ----------------------------------------------

    user = get_user(
        user_id
    )


    if not original_plan or user is None:

        raise HTTPException(
            status_code=404,
            detail="User or workout plan not found."
        )


    # ----------------------------------------------
    # UPDATE PLAN
    # ----------------------------------------------

    updated_plan = update_workout_plan(
        original_plan,
        feedback
    )


    # ----------------------------------------------
    # SAVE UPDATED PLAN
    # ----------------------------------------------

    save_updated_plan(
        user_id,
        updated_plan
    )


    # ----------------------------------------------
    # NUTRITION
    # ----------------------------------------------

    nutrition_tip = (
        generate_nutrition_tip_with_flash(
            user["goal"]
        )
    )


    # ----------------------------------------------
    # SHOW UPDATED RESULT
    # ----------------------------------------------

    return templates.TemplateResponse(

        request=request,

        name="result.html",

        context={

            "request": request,

            "username": user["name"],

            "user_id": user["id"],

            "age": user["age"],

            "weight": user["weight"],

            "goal": user["goal"],

            "intensity": user["intensity"],

            "workout_plan": updated_plan,

            "nutrition_tip": nutrition_tip,

            "updated": True
        }
    )


# ==================================================
# VIEW ALL USERS
# ==================================================

@router.get(
    "/view-all-users",
    response_class=HTMLResponse
)
def view_all_users(request: Request):

    users = get_all_users()

    plans = get_all_plans()


    # ----------------------------------------------
    # PLAN LOOKUP
    # ----------------------------------------------

    latest_plans = {}

    for plan in plans:

        if plan["user_id"] not in latest_plans:

            latest_plans[
                plan["user_id"]
            ] = plan


    # ----------------------------------------------
    # USER DATA
    # ----------------------------------------------

    user_data = []


    for user in users:

        plan = latest_plans.get(
            user["id"]
        )


        user_data.append({

            "id": user["id"],

            "name": user["name"],

            "age": user["age"],

            "weight": user["weight"],

            "goal": user["goal"],

            "intensity": user["intensity"],

            "original_plan":
                plan["original_plan"]
                if plan
                else "N/A",

            "updated_plan":
                plan["updated_plan"]
                if plan
                and plan["updated_plan"]
                else "Not updated"
        })


    # ----------------------------------------------
    # SHOW USERS
    # ----------------------------------------------

    return templates.TemplateResponse(

        request=request,

        name="all_users.html",

        context={

            "request": request,

            "users": user_data
        }
    )


# ==================================================
# GEMINI WORKOUT API
# ==================================================

@router.post(
    "/generate-workout/gemini"
)
def generate_gemini_workout(
    request: WorkoutRequest
):

    workout = generate_workout_gemini({

        "goal": request.goal,

        "intensity": request.intensity
    })


    return {

        "model": "FitBuddy AI",

        "workout_plan": workout
    }


# ==================================================
# NUTRITION API
# ==================================================

@router.get(
    "/nutrition-tip"
)
def get_flash_tip(goal: str):

    return {

        "goal": goal,

        "nutrition_tip":
            generate_nutrition_tip_with_flash(
                goal
            )
    }


# ==================================================
# GENERATE PLAN API
# ==================================================

@router.post(
    "/generate-plan"
)
def generate_plan_api(
    user_data: UserInput
):

    save_user(

        user_data.user_id,

        user_data.username,

        user_data.age,

        user_data.weight,

        user_data.goal,

        user_data.intensity
    )


    plan = generate_workout_gemini({

        "user_id":
            user_data.user_id,

        "name":
            user_data.username,

        "age":
            user_data.age,

        "weight":
            user_data.weight,

        "goal":
            user_data.goal,

        "intensity":
            user_data.intensity
    })


    save_plan(
        user_data.user_id,
        plan
    )


    return {

        "message":
            "Workout plan generated successfully!",

        "workout_plan":
            plan
    }


# ==================================================
# UPDATE PLAN API
# ==================================================

@router.post(
    "/update-plan/{user_id}"
)
def update_user_plan(

    user_id: int,

    data: FeedbackRequest
):

    original = get_original_plan(
        user_id
    )


    if not original:

        return {

            "error":
                "Original plan not found."
        }


    updated = update_workout_plan(

        original,

        data.feedback
    )


    save_updated_plan(

        user_id,

        updated
    )


    return {

        "updated_plan":
            updated
    }