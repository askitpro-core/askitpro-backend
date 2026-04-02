from pydantic import BaseModel, Field
from datetime import datetime

class Doubt(BaseModel):
    title: str
    description: str
    submitted_at: str = Field(default_factory=lambda: str(datetime.now()))