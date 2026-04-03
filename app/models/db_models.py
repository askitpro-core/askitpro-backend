from sqlalchemy import Column, Integer, String
from app.database import Base

class DoubtModel(Base):
    __tablename__ = "doubts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String) # Changed from description
    author_name = Column(String, index=True) # New
    room_code = Column(String, index=True) # New
    submitted_at = Column(String)
    upvotes = Column(Integer, default=0)
    cluster_id = Column(String, index=True)
    tag = Column(String)

class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    doubt_id = Column(Integer)
    user_id = Column(String)

