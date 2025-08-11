"""
Routers for user authentication, management, plan CRUD, and user-plan assignment.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from . import schemas, crud, auth

router = APIRouter(prefix="", tags=["Users and Plans"])


# ---------- User Registration & Authentication ----------

# PUBLIC_INTERFACE
@router.post("/auth/register", summary="Register a new user", response_model=schemas.UserRead, status_code=201)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    """
    Register a new user.
    """
    # Check if username or email taken
    existing_user = crud.get_user_by_username(db, user_in.username)
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already exists")
    # Would also check email in a real app
    user = crud.create_user(db, user_in)
    return crud.get_user_with_plan(db, user)

# PUBLIC_INTERFACE
@router.post("/auth/login", summary="Login and receive a JWT access token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(auth.get_db)):
    """
    Authenticate user and return JWT token if valid.
    """
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# ---------- User and Plan CRUD ----------

# PUBLIC_INTERFACE
@router.get("/users/me", summary="Get logged-in user profile", response_model=schemas.UserRead)
def read_users_me(current_user=Depends(auth.get_current_active_user), db: Session = Depends(auth.get_db)):
    """
    Get profile and assigned plan of logged-in user.
    """
    return crud.get_user_with_plan(db, current_user)

# PUBLIC_INTERFACE
@router.get("/users", summary="List all users", response_model=list[schemas.UserRead])
def list_all_users(db: Session = Depends(auth.get_db)):
    """
    List all registered users with their assigned plan (admin use).
    """
    users = crud.list_users(db)
    results = [crud.get_user_with_plan(db, user) for user in users]
    return results

# PUBLIC_INTERFACE
@router.delete("/users/{user_id}", summary="Delete a user", status_code=204)
def delete_user(user_id: int, db: Session = Depends(auth.get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return

# PUBLIC_INTERFACE
@router.post("/plans", summary="Create a new plan", response_model=schemas.PlanRead, status_code=201)
def create_plan(plan: schemas.PlanCreate, db: Session = Depends(auth.get_db)):
    """
    Add a new subscription plan.
    """
    existing = crud.get_plan_by_name(db, plan.name)
    if existing:
        raise HTTPException(status_code=409, detail="Plan name already exists")
    return crud.create_plan(db, plan)

# PUBLIC_INTERFACE
@router.get("/plans", summary="List all plans", response_model=list[schemas.PlanRead])
def list_plans(db: Session = Depends(auth.get_db)):
    """
    List all available plans.
    """
    return crud.list_plans(db)

# PUBLIC_INTERFACE
@router.post("/assign-plan", summary="Assign a plan to a user", response_model=schemas.PlanAssignment)
def assign_plan(
    user_id: int = Body(..., embed=True, description="User ID"),
    plan_id: int = Body(..., embed=True, description="Plan ID"),
    db: Session = Depends(auth.get_db)
):
    """
    Assign a subscription plan to a user.
    """
    user = crud.get_user_by_id(db, user_id)
    plan = crud.get_plan_by_id(db, plan_id)
    if not user or not plan:
        raise HTTPException(status_code=404, detail="User or plan not found")
    assignment = crud.assign_plan_to_user(db, user_id, plan_id)
    return {"user_id": assignment.user_id, "plan_id": assignment.plan_id}
