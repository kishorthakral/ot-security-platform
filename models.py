from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

technique_tactics = Table(
    "technique_tactics",
    Base.metadata,
    Column("technique_id", String, ForeignKey("techniques.id"), primary_key=True),
    Column("tactic_id", String, ForeignKey("tactics.id"), primary_key=True),
)

class Tactic(Base):
    __tablename__ = "tactics"

    id = Column(String, primary_key=True)  # e.g. "TA0108"
    name = Column(String, nullable=False)
    techniques = relationship("Technique", secondary=technique_tactics, back_populates="tactics")

class Technique(Base):
    __tablename__ = "techniques"

    id = Column(String, primary_key=True)  # e.g. "T0866"
    name = Column(String, nullable=False)
    priority = Column(String)
    asset = Column(String)
    description = Column(String)
    tactics = relationship("Tactic", secondary=technique_tactics, back_populates="techniques")