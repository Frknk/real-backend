from fastapi import FastAPI
from src.database import init_db
from contextlib import asynccontextmanager
from src.routes import root_router
from fastapi.middleware.cors import CORSMiddleware

from src.config import ALLOWED_ORIGIN

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    
def create_app():
    origins = [ALLOWED_ORIGIN]
    app = FastAPI(lifespan=lifespan)
    app.include_router(root_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app