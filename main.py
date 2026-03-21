from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import doubt_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(doubt_routes.router)

@app.get("/ping")
def ping():
    return {"status": "API is live"}
