from datetime import date

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
