from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Doubt(BaseModel):
    text: str
    author_name: str
    room_code: str
    submitted_at: Optional[str] = None

    def __init__(self, **data):
        if "submitted_at" not in data or not data["submitted_at"]:
            data["submitted_at"] = str(datetime.now())
        super().__init__(**data)