# ./app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.db import init_db, seed_db
from app.modules.users.routers import router as users_router
from app.modules.doctors.routers import router as doctors_router
from app.modules.schedules.routers import router as schedules_router
from app.modules.preferences.routers import router as preferences_router
from app.modules.swap_requests.routers import router as swap_requests_router
from app.modules.stats.routers import router as stats_router

app = FastAPI(
    title="Duty Schedule API",
    description="API for managing doctor duty schedules",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users_router)
app.include_router(doctors_router)
app.include_router(schedules_router)
app.include_router(preferences_router)
app.include_router(swap_requests_router)
app.include_router(stats_router)


@app.on_event("startup")
async def startup():
    init_db()
    seed_db()  # <-- Добавляем вызов seed


@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/debug/users")
async def debug_users():
    """Временный эндпоинт для проверки что пользователи создались"""
    from sqlmodel import Session, select
    from app.core.db import engine
    from app.modules.users.models import User
    
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return {
            "count": len(users),
            "users": [{"email": u.email, "role": u.role} for u in users]
        }