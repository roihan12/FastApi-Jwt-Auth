from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.routers import router

from src.database import engine, Base

app = FastAPI(default_response_class=ORJSONResponse)
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(router)