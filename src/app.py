from fastapi import FastAPI
from src.database import init_db
from contextlib import asynccontextmanager
from src.routes import root_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    
def create_app():
    app = FastAPI(lifespan=lifespan)
    app.include_router(root_router)
    return app