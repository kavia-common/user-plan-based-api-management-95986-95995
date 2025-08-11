"""
Resource endpoint whose behavior changes according to current user's plan - in-memory.
"""
from fastapi import APIRouter, HTTPException, Depends
from . import auth

router = APIRouter(
    prefix="",
    tags=["Resource"],
)

# PUBLIC_INTERFACE
@router.get("/resource", summary="Get resource, differing by user's assigned plan")
def get_resource(
    current_user: dict = Depends(auth.get_current_active_user)
):
    """
    Returns a response string depending on the logged-in user's assigned plan.
    - BASIC: summary usage only.
    - PRO: summary plus analytics.
    - ENTERPRISE: full insights and downloads.
    """
    plan = current_user.get("plan")
    if not plan:
        raise HTTPException(status_code=403, detail="User has no plan assigned")

    plan = plan.upper()
    if plan == "BASIC":
        return {"message": f"Hello {current_user['username']} (BASIC). You have basic access: summary usage report only."}
    elif plan == "PRO":
        return {"message": f"Hello {current_user['username']} (PRO). You get pro access: summary report plus analytics."}
    elif plan == "ENTERPRISE":
        return {"message": f"Hello {current_user['username']} (ENTERPRISE). You get full enterprise insights and downloads!"}
    else:
        return {"message": f"Unknown plan type: {plan}"}
