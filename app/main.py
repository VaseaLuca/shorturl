from fastapi import FastAPI
from app.models.short_url import Base as ShortURLBase
from app.dependencies.database import engine, SessionLocal
from app.routers.short_url import router as short_url_router

app = FastAPI()
ShortURLBase.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(short_url_router)

@app.get("/")

async def root():
    return {"message": "Hello Bugs :)"}