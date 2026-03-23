from sqlalchemy import Column, Integer, String
from app.database import Base

class DoubtModel(Base):
    __tablename__ = "doubts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    submitted_at = Column(String)
    upvotes = Column(Integer, default=0)