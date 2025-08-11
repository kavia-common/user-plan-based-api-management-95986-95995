"""
CRUD and business logic for users, plans, and user-plan assignments - in-memory.
"""
from typing import Optional, List
from . import schemas, auth

# --- User CRUD ---

# PUBLIC_INTERFACE
def create_user(user_in: schemas.UserCreate) -> dict:
    # Only for demo - append user to in-memory store.
    next_id = max([u["id"] for u in auth.USERS]) + 1
    user = {
        "id": next_id,
        "username": user_in.username,
        "email": user_in.email,
        "password": user_in.password,
        "plan": "BASIC"  # Auto-assign BASIC plan
    }
    auth.USERS.append(user)
    auth.username_to_user[user["username"]] = user
    auth.id_to_user[user["id"]] = user
    return user

# PUBLIC_INTERFACE
def get_user_by_username(username: str) -> Optional[dict]:
    return auth.username_to_user.get(username)

# PUBLIC_INTERFACE
def get_user_by_id(user_id: int) -> Optional[dict]:
    return auth.id_to_user.get(user_id)

# PUBLIC_INTERFACE
def list_users() -> List[dict]:
    return list(auth.USERS)

# PUBLIC_INTERFACE
def delete_user(user_id: int) -> bool:
    user = auth.id_to_user.get(user_id)
    if user:
        auth.USERS.remove(user)
        del auth.username_to_user[user["username"]]
        del auth.id_to_user[user["id"]]
        return True
    return False

# --- Plan CRUD ---

# PUBLIC_INTERFACE
def create_plan(plan_in: schemas.PlanCreate) -> dict:
    # Only allow new plans by admin (demonstration)
    next_id = max([p["id"] for p in auth.PLANS]) + 1
    plan = {
        "id": next_id,
        "name": plan_in.name,
        "description": plan_in.description
    }
    auth.PLANS.append(plan)
    auth.plan_name_to_plan[plan["name"]] = plan
    auth.id_to_plan[plan["id"]] = plan
    return plan

# PUBLIC_INTERFACE
def get_plan_by_name(name: str) -> Optional[dict]:
    return auth.plan_name_to_plan.get(name)

# PUBLIC_INTERFACE
def get_plan_by_id(plan_id: int) -> Optional[dict]:
    return auth.id_to_plan.get(plan_id)

# PUBLIC_INTERFACE
def list_plans() -> List[dict]:
    return list(auth.PLANS)

# --- Plan Assignment ---

# PUBLIC_INTERFACE
def assign_plan_to_user(user_id: int, plan_id: int):
    user = get_user_by_id(user_id)
    plan = get_plan_by_id(plan_id)
    if user and plan:
        user["plan"] = plan["name"]
        return {"user_id": user_id, "plan_id": plan_id}
    return None

# PUBLIC_INTERFACE
def get_user_with_plan(user: dict) -> schemas.UserRead:
    # Return UserRead schema from dict
    return schemas.UserRead(
        id=user["id"],
        username=user["username"],
        email=user["email"],
        plan=user.get("plan")
    )
