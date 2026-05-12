from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import create_db_and_tables
from app.routes import posts


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.
    Creates database tables on startup.
    """
    await create_db_and_tables()
    yield


app = FastAPI(
    title="Posts API",
    description="API para upload e gerenciamento de posts com imagens e vídeos",
    version="1.0.0",
    lifespan=lifespan
)


# Include routers
app.include_router(posts.router)


@app.get("/")
async def root():
    """
    Root endpoint - API health check.
    """
    return {
        "message": "Posts API is running",
        "docs": "/docs",
        "redoc": "/redoc"
    }
