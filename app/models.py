from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
import uuid
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    ccurrent_session_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"))
    text = Column(String(255))
    word_count = Column(Integer)
    uppercase_count = Column(Integer)
    special_character_count = Column(Integer)
    user = relationship("User", back_populates="analyses")  