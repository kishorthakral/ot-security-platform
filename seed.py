from sqlalchemy.orm import Session
from database import engine
from models import Tactic, Technique

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


TECHNIQUES = [
    {"id": "T0866", "name": "Exploitation of Remote Services", "tactics": ["TA0108", "TA0109"],
     "priority": "H", "asset": "ITOT", "description": "Software vulnerability exploited to abuse a remote service."},
    {"id": "T0859", "name": "Valid Accounts", "tactics": ["TA0110", "TA0109"],
     "priority": "H", "asset": "GEN", "description": "Stolen legitimate credentials used to bypass access controls."},
    {"id": "T0836", "name": "Modify Parameter", "tactics": ["TA0106"],
     "priority": "C", "asset": "PLC", "description": "Device parameters altered to change how actions execute."},
    {"id": "T0843", "name": "Program Download", "tactics": ["TA0109"],
     "priority": "C", "asset": "PLC", "description": "A user program transferred to a controller, overwriting logic."},
    
]

def seed_techniques():
    with Session(engine) as session:
        for item in TECHNIQUES:
            if session.get(Technique, item["id"]) is None:
                technique = Technique(
                    id=item["id"],
                    name=item["name"],
                    priority=item["priority"],
                    asset=item["asset"],
                    description=item["description"],
                )
                session.add(technique)
                for tactic_id in item["tactics"]:
                    tactic = session.get(Tactic, tactic_id)
                    if tactic is None:
                        raise ValueError(f"Unknown tactic {tactic_id} for technique {item['id']}")
                    technique.tactics.append(tactic)
        session.commit()
    print("Techniques seeded successfully.")

if __name__ == "__main__":
    seed_tactics()
    seed_techniques()