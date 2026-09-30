
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import init_db
from routes import router

app = FastAPI(
    title="FitBuddy AI",
    description="Your Personal AI Fitness Planner",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

init_db()
app.include_router(router)