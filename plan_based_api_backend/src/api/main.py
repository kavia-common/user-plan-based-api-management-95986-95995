from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .models import Base
from .routers_auth import router as auth_router
from .routers_plans import router as plans_router
from .routers_resource import router as resource_router

app = FastAPI(
    title="Plan-Based API Backend",
    description="Backend API for user, plan, and resource management with plan-based endpoint behavior.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Authentication", "description": "User registration and login"},
        {"name": "Plans", "description": "API plans and user-plan assignment"},
        {"name": "Resource", "description": "Endpoints whose behavior changes with user plan"}
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB tables at startup if not present
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Health check endpoint
@app.get("/", tags=["Monitoring"])
def health_check():
    """Health check endpoint."""
    return {"message": "Healthy"}

# Register main API routers
app.include_router(auth_router)
app.include_router(plans_router)
app.include_router(resource_router)
