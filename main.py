from fastapi import FastAPI
from sqlalchemy.orm import Session
from database import engine
from models import Technique

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "OT Security Platform API  is running"}

@app.get("/techniques")
def list_techniques():
    with Session(engine) as session:
        techniques = session.query(Technique).order_by(Technique.id).all()
        return [
            {
                "id": t.id,
                "name": t.name,
                "priority": t.priority,
                "asset": t.asset,
                "description": t.description,
                "tactics": [tactic.name for tactic in t.tactics],
            }
            for t in techniques
        ]
