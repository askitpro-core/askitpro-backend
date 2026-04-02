from app.services.ai_engine import find_cluster_for_doubt, generate_auto_tag
from pydantic import BaseModel
from datetime import datetime

class Doubt(BaseModel):
    title: str
    description: str
    submitted_at: str = ""

    def __init__(self, **data):
        if "submitted_at" not in data:
            data["submitted_at"] = str(datetime.now())
        super().__init__(**data)
