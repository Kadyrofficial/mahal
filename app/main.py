from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

from api import router, ws_router
from db import db_helper
from models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    lifespan=lifespan,
    title="Mahal",
    version="1.0.0",
    description="Mahal Economic Society"
)
@app.get(path="/")
def get_home():
    return "Hi"
app.include_router(router)
app.include_router(ws_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
