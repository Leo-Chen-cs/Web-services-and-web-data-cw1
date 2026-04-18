"""Pydantic schemas for User authentication."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserSchemaConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
    )


class UserCreate(UserSchemaConfig):
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8, max_length=128, description="Password (8-128 characters)")

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not value.replace("_", "").replace("-", "").isalnum():
            raise ValueError("Username may only contain letters, numbers, underscores, and hyphens")
        return value

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        has_alpha = any(char.isalpha() for char in value)
        has_digit = any(char.isdigit() for char in value)
        if not (has_alpha and has_digit):
            raise ValueError("Password must include at least one letter and one number")
        return value


class UserResponse(UserSchemaConfig):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool
    created_at: Optional[datetime] = None


class UserLogin(UserSchemaConfig):
    username: str
    password: str


class Token(UserSchemaConfig):
    access_token: str
    token_type: str = "bearer"


class TokenData(UserSchemaConfig):
    username: Optional[str] = None
