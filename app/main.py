from fastapi import FastAPI

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.routes import doubt_routes
from app.models import db_models
from app.database import engine, Base
from app.routes.ws import router as ws_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AskItPro API",
    version="2.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(doubt_routes.router)
app.include_router(ws_router)


@app.get("/")
def read_root():
    return {"message": "API is live"}

@app.get("/ping")
def ping():
    return {"status": "API is live"}


class Doubt(BaseModel):
    title: str
    description: str