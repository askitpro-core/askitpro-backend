from fastapi import FastAPI
from app.routes import doubt_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(doubt_routes.router)

@app.get("/ping")
def ping():
    return {"status": "API is live"}