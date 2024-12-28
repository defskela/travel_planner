from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class RouteResponse(BaseModel):
    id: int
    name: str
    place: str
    weather: str
    date: date

    class Config:
        orm_mode = True


class RouteCreate(BaseModel):
    name: str
    place: str
    weather: str
    date: date


class RouteUpdate(BaseModel):
    name: Optional[str]
    place: Optional[str]
    weather: Optional[str]
    date: Optional[date]
