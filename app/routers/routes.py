from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.jwt import get_current_user
from app.models import Route as RouteModel
from app.models import User
from app.schemas import RouteCreate, RouteResponse

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

    if existing_route:
        raise HTTPException(
            status_code=400, detail="Route with this name already exists")

    new_route = RouteModel(
        name=route.name,
        place=route.place,
        weather=route.weather,
        date=route.date,
        user_id=current_user.id
    )

    db.add(new_route)
    await db.commit()
    await db.refresh(new_route)

    return new_route
