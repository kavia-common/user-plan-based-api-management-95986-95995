from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from . import auth

router = APIRouter(
    prefix="/resource",
    tags=["Resource"],
)

# PUBLIC_INTERFACE
@router.get("/fetch_data", summary="Fetch resource, plan-based logic")
def fetch_data(
    db: Session = Depends(get_db),
    user=Depends(auth.get_current_user),
):
    """
    Returns data according to user's assigned plan.
    Free plan: simple message. 
    Pro plan: includes extra features.
    Enterprise plan: includes all features.
    """
    plan = auth.get_user_plan(db, user)
    if not plan:
        raise HTTPException(status_code=403, detail="No plan assigned")

    # Plan-based logic
    if plan.name.lower() == "free":
        return {"message": "Welcome Free user. Basic access."}
    elif plan.name.lower() == "pro":
        return {"message": "Hello Pro user! You get basic + advanced features."}
    elif plan.name.lower() == "enterprise":
        return {"message": "Hello Enterprise user! You have full access to all features."}
    else:
        return {"message": f"Plan '{plan.name}' is not recognized."}
