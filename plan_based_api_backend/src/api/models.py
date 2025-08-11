from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# PUBLIC_INTERFACE
class Plan(Base):
    """Subscription plan model."""
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    users = relationship("UserPlan", back_populates="plan")

# PUBLIC_INTERFACE
class User(Base):
    """User model."""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    plans = relationship("UserPlan", back_populates="user")

# PUBLIC_INTERFACE
class UserPlan(Base):
    """Assignment of users to plans."""
    __tablename__ = "user_plans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    assigned_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="plans")
    plan = relationship("Plan", back_populates="users")
