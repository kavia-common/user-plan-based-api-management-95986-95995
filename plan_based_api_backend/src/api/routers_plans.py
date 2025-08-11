from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from . import schemas, models, auth

router = APIRouter(
    prefix="/plans",
    tags=["Plans"],
)

# PUBLIC_INTERFACE
@router.post("/", summary="Create a new plan", response_model=schemas.PlanResponse)
def create_plan(plan: schemas.PlanCreate, db: Session = Depends(get_db)):
    """Create a new API plan."""
    if db.query(models.Plan).filter(models.Plan.name == plan.name).first():
        raise HTTPException(status_code=400, detail="Plan with this name already exists")
    plan_db = models.Plan(name=plan.name, description=plan.description)
    db.add(plan_db)
    db.commit()
    db.refresh(plan_db)
    return plan_db

# PUBLIC_INTERFACE
@router.get("/", summary="List all plans", response_model=list[schemas.PlanResponse])
def list_plans(db: Session = Depends(get_db)):
    """List all available plans."""
    return db.query(models.Plan).all()

# PUBLIC_INTERFACE
@router.post("/assign", summary="Assign plan to user")
def assign_plan(request: schemas.AssignPlanRequest, db: Session = Depends(get_db)):
    """Assign a plan to a user."""
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    plan = db.query(models.Plan).filter(models.Plan.name == request.plan_name).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    user_plan = models.UserPlan(user_id=user.id, plan_id=plan.id)
    db.add(user_plan)
    db.commit()
    return {"msg": f"Plan '{plan.name}' assigned to user '{user.username}'."}

# PUBLIC_INTERFACE
@router.get("/user/{username}", summary="Get current plan for user")
def get_user_current_plan(username: str, db: Session = Depends(get_db)):
    """Get the current plan assigned to a user."""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    plan = auth.get_user_plan(db, user)
    if not plan:
        return {"plan": None}
    return {"plan": plan.name}
