from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import database
from app.routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    yield


app = FastAPI(
    title="Short Link Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)


