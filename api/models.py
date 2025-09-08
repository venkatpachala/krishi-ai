from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from .db import Base

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    source = Column(String)
    content = Column(String)
    embedding = Column(Vector(3072))

class QueryLog(Base):
    __tablename__ = "query_logs"
    id = Column(Integer, primary_key=True, index=True)
    query = Column(String)
    answer = Column(String)
    confidence = Column(Float)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    feedback = relationship("Feedback", back_populates="query_log")

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, ForeignKey("query_logs.id"))
    rating = Column(Integer)
    comment = Column(String, nullable=True)
    query_log = relationship("QueryLog", back_populates="feedback")

class Officer(Base):
    __tablename__ = "officers"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    lat = Column(Float)
    lon = Column(Float)
