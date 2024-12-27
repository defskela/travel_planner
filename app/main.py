from fastapi import FastAPI

from app.database import engine
from app.models import Base
from app.routers import auth

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Подключение роутеров
app.include_router(auth.router)
