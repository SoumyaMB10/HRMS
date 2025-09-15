from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings
from src.db.session import engine
from src.db.base import Base
from src.api import auth, attendance, leaves, policies, manager, recruitment, resignation, payroll, users

app = FastAPI(title="HRMS API (full flows)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(recruitment.router)
app.include_router(resignation.router)
app.include_router(payroll.router)
app.include_router(attendance.router)
app.include_router(leaves.router)
app.include_router(policies.router)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
