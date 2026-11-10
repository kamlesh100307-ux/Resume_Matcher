from sqlalchemy import Column, Integer, String, Text, Float
from database import base

class users(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

class jobs(base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    required_skills = Column(Text, nullable=False)
    min_experience = Column(Float, default=0)
    max_experience = Column(Float, default=2)
