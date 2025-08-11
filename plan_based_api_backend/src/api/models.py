"""
SQLAlchemy models and user password helpers for plan-based API backend.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base
from passlib.context import CryptContext

Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    plan_assignment = relationship("UserPlan", back_populates="user", uselist=False)

    # PUBLIC_INTERFACE
    def verify_password(self, password: str) -> bool:
        """Verify provided password with stored hashed password."""
        return pwd_context.verify(password, self.hashed_password)

    # PUBLIC_INTERFACE
    @classmethod
    def get_password_hash(cls, password: str) -> str:
        """Hash a plain password for storage."""
        return pwd_context.hash(password)


class Plan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    users = relationship("UserPlan", back_populates="plan")


class UserPlan(Base):
    __tablename__ = "user_plans"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    user = relationship("User", back_populates="plan_assignment")
    plan = relationship("Plan", back_populates="users")
    __table_args__ = (UniqueConstraint('user_id'),)
