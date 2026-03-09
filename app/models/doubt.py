from pydantic import BaseModel

class Doubt(BaseModel):
    title: str
    description: str