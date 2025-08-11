from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

router = APIRouter(
    prefix="",
    tags=["Resource"],
)

# Hardcoded user data for this demo
HARDCODED_USERS = [
    {"id": 1, "username": "alice", "name": "Alice", "plan": "Free"},
    {"id": 2, "username": "bob", "name": "Bob", "plan": "Pro"},
    {"id": 3, "username": "charlie", "name": "Charlie", "plan": "Enterprise"},
]

# Mapping for quick lookup
USERS_BY_USERNAME = {u["username"]: u for u in HARDCODED_USERS}
USERS_BY_ID = {u["id"]: u for u in HARDCODED_USERS}


class UserPlanResponse(BaseModel):
    """Response model showing the user's plan information."""
    id: int = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    name: str = Field(..., description="User's display name")
    plan: str = Field(..., description="User's assigned plan (Free, Pro, Enterprise)")


# PUBLIC_INTERFACE
@router.get(
    "/plan",
    response_model=UserPlanResponse,
    summary="Get user's plan by username or ID",
    description="Retrieve the assigned plan for a user, looked up by username or user_id. Returns 404 if user not found.",
    tags=["Resource"],
    responses={
        404: {"description": "User not found"}
    }
)
def get_user_plan(
    username: Optional[str] = Query(None, description="Username of user"),
    user_id: Optional[int] = Query(None, description="User ID")
):
    """
    Returns the plan for one of three hardcoded users, looked up by username or user_id.
    Example users:
    - id: 1, username: alice, plan: Free
    - id: 2, username: bob, plan: Pro
    - id: 3, username: charlie, plan: Enterprise

    You must supply either username or user_id.
    """
    # Prioritize username lookup for this example, otherwise use user_id.
    user = None
    if username:
        user = USERS_BY_USERNAME.get(username.lower())
    elif user_id:
        user = USERS_BY_ID.get(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # Return the user's plan details
    return UserPlanResponse(**user)


# Retain the original demo endpoint for plan-differentiated messages
# PUBLIC_INTERFACE
@router.get("/resource", summary="Get resource response based on user's plan")
def resource(username: str = Query(..., description="Username to check")):
    """
    Returns a response string depending on which hardcoded user is supplied. (Legacy/demo style endpoint)
    - alice: plan BASIC
    - bob: plan PRO
    - clara: plan ENTERPRISE
    """
    users_and_plans = {
        "alice": {"plan": "BASIC"},
        "bob": {"plan": "PRO"},
        "clara": {"plan": "ENTERPRISE"},
    }
    user_plan = users_and_plans.get(username)
    if not user_plan:
        raise HTTPException(status_code=404, detail="Unknown user or user not configured in demo.")

    plan = user_plan["plan"]
    if plan == "BASIC":
        return {"message": "Hello Alice (BASIC). You have basic access: summary usage report only."}
    elif plan == "PRO":
        return {"message": "Hello Bob (PRO). You get pro access: summary report plus analytics."}
    elif plan == "ENTERPRISE":
        return {"message": "Hello Clara (ENTERPRISE). You get full enterprise insights and downloads!"}
    else:
        return {"message": f"Unknown plan type: {plan}"}
