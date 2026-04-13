from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str
    picture_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Purchase(SQLModel, table=True):
    __tablename__ = "purchases"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    week_id: str = Field(default="week5")
    polar_checkout_id: Optional[str] = None
    status: str = Field(default="pending")  # pending | completed | failed
    purchased_at: Optional[datetime] = None


class RefreshToken(SQLModel, table=True):
    __tablename__ = "refresh_tokens"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    token: str = Field(unique=True)
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
