from sqlalchemy import create_engine, event
from models import Base

engine = create_engine("sqlite:///ot_platform.db")

@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Database and tables created successfully.")