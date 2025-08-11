"""
CRUD and business logic for users, plans, and user-plan assignments.
"""
from typing import Optional
from sqlalchemy.orm import Session
from . import models, schemas, auth

# PUBLIC_INTERFACE
def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    """Create a new user (with hashed password)."""
    hashed_pw = auth.get_password_hash(user_in.password)
    user = models.User(username=user_in.username, email=user_in.email, hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# PUBLIC_INTERFACE
def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

# PUBLIC_INTERFACE
def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

# PUBLIC_INTERFACE
def list_users(db: Session):
    return db.query(models.User).all()

# PUBLIC_INTERFACE
def create_plan(db: Session, plan_in: schemas.PlanCreate) -> models.Plan:
    plan = models.Plan(name=plan_in.name, description=plan_in.description)
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan

# PUBLIC_INTERFACE
def get_plan_by_name(db: Session, name: str) -> Optional[models.Plan]:
    return db.query(models.Plan).filter(models.Plan.name == name).first()

# PUBLIC_INTERFACE
def get_plan_by_id(db: Session, plan_id: int) -> Optional[models.Plan]:
    return db.query(models.Plan).filter(models.Plan.id == plan_id).first()

# PUBLIC_INTERFACE
def list_plans(db: Session):
    return db.query(models.Plan).all()

# PUBLIC_INTERFACE
def assign_plan_to_user(db: Session, user_id: int, plan_id: int):
    assignment = db.query(models.UserPlan).filter_by(user_id=user_id).first()
    if assignment:
        assignment.plan_id = plan_id
        db.commit()
        db.refresh(assignment)
        return assignment
    assignment = models.UserPlan(user_id=user_id, plan_id=plan_id)
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment

# PUBLIC_INTERFACE
def get_user_with_plan(db: Session, user: models.User):
    plan_name = None
    if user.plan_assignment and user.plan_assignment.plan:
        plan_name = user.plan_assignment.plan.name
    return schemas.UserRead(
        id=user.id,
        username=user.username,
        email=user.email,
        plan=plan_name
    )
