"""Sets up connection to Postgres"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql+psycopg2://titanbay:titanbay@localhost:5432/titanbay_funds"

# Set up connection to Postgres
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Opens a session, hands it over, and closes it after automatically. Used with FastAPI so every endpoint has a
# Working session without manual setup each time
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()