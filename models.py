from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Technique(Base):
    __tablename__ = 'techniques'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    tactic = Column(String, nullable=False)
    priority = Column(String, nullable=False)
    asset = Column(String, nullable=False)
    description = Column(String, nullable=False)    