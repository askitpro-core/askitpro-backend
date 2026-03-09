from fastapi import FastAPI
from app.routes import doubt_routes

app = FastAPI()

app.include_router(doubt_routes.router)

@app.get("/ping")
def ping():
    return {"status": "API is live"}