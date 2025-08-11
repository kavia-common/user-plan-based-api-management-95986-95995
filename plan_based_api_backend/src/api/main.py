"""
FastAPI main entrypoint for plan-based API backend.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers_resource import router as resource_router
from .routers_users_plans import router as users_plans_router
from .database import engine
from .models import Base

# Create all tables on startup (dev/demo only). Production: use Alembic.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Plan-Based API Backend (Demo Mode)",
    description="Backend API with real user authentication, plan management, and plan-based endpoint behavior.",
    version="1.0.1",
    openapi_tags=[
        {"name": "Resource", "description": "Endpoints whose behavior change based on user's plan"},
        {"name": "Users and Plans", "description": "User authentication, management, and plan assignment"}
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Monitoring"])
def health_check():
    """Health check endpoint."""
    return {"message": "Healthy"}

app.include_router(users_plans_router)
app.include_router(resource_router)
