from sqlalchemy.orm import Session
from database import engine
from models import Tactic

TACTICS = [
    ("TA0108", "Initial Access"),
    ("TA0104", "Execution"),
    ("TA0110", "Persistence"),
    ("TA0111", "Privilege Escalation"),
    ("TA0103", "Evasion"),
    ("TA0102", "Discovery"),
    ("TA0109", "Lateral Movement"),
    ("TA0100", "Collection"),
    ("TA0101", "Command and Control"),
    ("TA0107", "Inhibit Response Function"),
    ("TA0106", "Impair Process Control"),
    ("TA0105", "Impact"),
]

def seed_tactics():
    with Session(engine) as session:
        for tactic_id, tactic_name in TACTICS:
            tactic = Tactic(id=tactic_id, name=tactic_name)
            if session.get(Tactic, tactic_id) is None:  # Check if the tactic already exists
                session.add(tactic)
        session.commit()
    print("Tactics seeded successfully.")

if __name__ == "__main__":
    seed_tactics()