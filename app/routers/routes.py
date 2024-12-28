from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.jwt import get_current_user
from app.models import Route as RouteModel
from app.models import User
from app.schemas import RouteCreate, RouteResponse, RouteUpdate
from app.utils import get_weather

router = APIRouter(
    prefix="/routes",
    tags=["routes"]
)


@router.get("/getRoutes", response_model=List[RouteResponse])
async def get_routes(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RouteModel).where(RouteModel.user_id == current_user.id))
    routes = result.scalars().all()
    return routes


@router.post("/createRoute", response_model=RouteResponse)
async def create_route(route: RouteCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RouteModel).where(RouteModel.name == route.name))
    existing_route = result.scalars().first()

    new_route = RouteModel(
        name=route.name,
        place=route.place,
        weather=get_weather(route.place),
        date=route.date,
        user_id=current_user.id
    )

    db.add(new_route)
    await db.commit()
    await db.refresh(new_route)

    return new_route


@router.patch("/updateRoute/{route_id}", response_model=RouteResponse)
async def update_route(route_id: int, route: RouteUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RouteModel).where(RouteModel.id == route_id, RouteModel.user_id == current_user.id))
    existing_route = result.scalars().first()

    if not existing_route:
        raise HTTPException(status_code=404, detail="Route not found")

    if route.name is not None:
        existing_route.name = route.name
    if route.place is not None:
        existing_route.place = route.place
    if route.date is not None:
        existing_route.date = route.date
    weather = get_weather(existing_route.place)
    existing_route.weather = weather

    await db.commit()
    await db.refresh(existing_route)

    return existing_route


@router.delete("/deleteRoute/{route_id}", response_model=dict)
async def delete_route(route_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RouteModel).where(RouteModel.id == route_id, RouteModel.user_id == current_user.id))
    existing_route = result.scalars().first()

    if not existing_route:
        raise HTTPException(status_code=404, detail="Route not found")

    await db.delete(existing_route)
    await db.commit()

    return {"detail": "Route deleted successfully"}
