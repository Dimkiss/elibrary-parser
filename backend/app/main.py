from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import articles
from app.db import engine
from app.models import Base

app = FastAPI(
    title="Elibrary Parser API",
    description="API для парсинга и обработки данных по DOI",
)

origins = [
    "http://localhost",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(articles.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
