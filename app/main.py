from fastapi import FastAPI
from .routes import router
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener")

app.include_router(router)
