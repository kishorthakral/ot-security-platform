import json
from collections import Counter
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

EXPECTED_PER_TACTIC = {
    "TA0108": 12, "TA0104": 10, "TA0110": 5, "TA0111": 2, "TA0103": 7, "TA0102": 5,
    "TA0109": 6, "TA0100": 11, "TA0101": 3, "TA0107": 13, "TA0106": 4, "TA0105": 12,
}

def seed_tactics():
    with Session(engine) as session:
        for tactic_id, tactic_name in TACTICS:
            tactic = Tactic(id=tactic_id, name=tactic_name)
            if session.get(Tactic, tactic_id) is None:  # Check if the tactic already exists
                session.add(tactic)
        session.commit()
    print("Tactics seeded successfully.")

def load_techniques(path="techniques.json"):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    validate_techniques(data)
    return data

def validate_techniques(data):
    for t in data:
        for field in ("id", "name", "tactics"):
            if field not in t:
                raise ValueError(f"Technique {t.get('id', '?')} is missing field '{field}'")
        if not t["tactics"]:
            raise ValueError(f"Technique {t['id']} has no tactics")
    
    known_tactics = {tactic_id for tactic_id, _ in TACTICS}
    id_counts = Counter(t["id"] for t in data)
    duplicates = [tech_id for tech_id, n in id_counts.items() if n > 1]
    if duplicates:
        raise ValueError(f"Duplicate technique IDs: {duplicates}")

    actual = Counter(tactic_id for t in data for tactic_id in t["tactics"])

    for t in data:
        for tactic_id in t["tactics"]:
            if tactic_id not in known_tactics:
                raise ValueError(f"Unknown tactic {tactic_id} in technique {t['id']}")

    for tactic_id, expected in EXPECTED_PER_TACTIC.items():
        if actual[tactic_id] != expected:
            raise ValueError(f"{tactic_id}: expected {expected} techniques, found {actual[tactic_id]}")

def seed_techniques():
    with Session(engine) as session:
        for item in load_techniques():
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