from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers_resource import router as resource_router

app = FastAPI(
    title="Plan-Based API Backend (Demo Mode)",
    description="Backend API with hardcoded user-plan logic. Users: alice (BASIC), bob (PRO), clara (ENTERPRISE). Endpoint /resource?username=<user> is plan-aware.",
    version="1.0.1",
    openapi_tags=[
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

@app.get("/", tags=["Monitoring"])
def health_check():
    """Health check endpoint."""
    return {"message": "Healthy"}

# Only register the new resource router for this demo.
app.include_router(resource_router)
