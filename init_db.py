# init_db.py
from app.core.database import engine
from app.core.models import Base

def init_db():
    print("Initializing database and creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Database initialization complete.")

if __name__ == "__main__":
    init_db()
