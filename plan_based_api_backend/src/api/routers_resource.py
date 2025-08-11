from fastapi import APIRouter, Query, HTTPException

router = APIRouter(
    prefix="",
    tags=["Resource"],
)

# Hardcoded user->plan mapping
USERS_AND_PLANS = {
    "alice": {"plan": "BASIC"},
    "bob": {"plan": "PRO"},
    "clara": {"plan": "ENTERPRISE"},
}

# PUBLIC_INTERFACE
@router.get("/resource", summary="Get resource response based on user's plan")
def resource(username: str = Query(..., description="Username to check")):
    """
    Returns a response string depending on which hardcoded user is supplied.
    - alice: plan BASIC
    - bob: plan PRO
    - clara: plan ENTERPRISE
    """
    user_plan = USERS_AND_PLANS.get(username)
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
