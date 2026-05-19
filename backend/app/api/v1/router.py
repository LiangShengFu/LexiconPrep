from fastapi import APIRouter

from app.api.v1 import auth, users, questions, mistakes, flashcards, resources, stats

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(questions.router)
api_router.include_router(mistakes.router)
api_router.include_router(flashcards.router)
api_router.include_router(resources.router)
api_router.include_router(stats.router)
