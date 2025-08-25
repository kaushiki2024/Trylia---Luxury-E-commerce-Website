from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# Shared
class Message(BaseModel):
    message: str


# User
class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserRead(UserBase):
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: int


# Photo
class UserPhotoCreate(BaseModel):
    image_url: str


class UserPhotoRead(BaseModel):
    photo_id: int
    user_id: int
    image_url: str
    uploaded_at: datetime

    class Config:
        from_attributes = True


# Outfit
class OutfitBase(BaseModel):
    name: str
    category: str
    image_url: str
    metadata: dict = {}


class OutfitCreate(OutfitBase):
    pass


class OutfitUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    metadata: Optional[dict] = None


class OutfitRead(OutfitBase):
    outfit_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Outfit3DRead(BaseModel):
    id: int = Field(alias="model_id")
    outfit_id: int
    file_url: str
    format: str
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True


# TryOnSession
class TryOnSessionCreate(BaseModel):
    photo_id: Optional[int] = None
    outfit_id: Optional[int] = None
    result_url: Optional[str] = None


class TryOnSessionRead(BaseModel):
    session_id: int
    user_id: int
    photo_id: Optional[int]
    outfit_id: Optional[int]
    result_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# Recommendation
class RecommendationCreate(BaseModel):
    outfit_id: int
    score: int = Field(ge=0, le=100)


class RecommendationRead(BaseModel):
    rec_id: int
    user_id: int
    outfit_id: int
    score: int
    created_at: datetime

    class Config:
        from_attributes = True

