from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.jwt import get_current_user
from app.models import Route as RouteModel
from app.models import User
from app.schemas import RouteResponse

router = APIRouter(
    prefix="/routes",
    tags=["routes"]
)


@router.get("/", response_model=List[RouteResponse])
async def get_routes(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RouteModel).where(RouteModel.user_id == current_user.id))
    routes = result.scalars().all()
    return routes
