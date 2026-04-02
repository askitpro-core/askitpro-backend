from fastapi import FastAPI
from pydantic import BaseModel
from app.routes.doubt_routes import router

app = FastAPI(
    title="AskItPro API",
    version="2.0.0"
)

@app.get("/")
def read_root():
    return {"message": "API is live"}


class Doubt(BaseModel):
    title: str
    description: str
app.include_router(router)



