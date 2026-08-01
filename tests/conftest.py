import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

# Create separate, temporary SQLite database in memory, to run tests on. SQLite used as it doesn't require database server to be running
TEST_DATABASE_URL = "sqlite:///:memory:"

# Connection to SQLite database to run tests on
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture()
def client():
    # Runs at start of every test to create empty tables in the in-memory test database
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    # Swap out get_db (which connects to real Postgres database) to point at test in-memory SQLite database instead
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

    # Drop tables after test is finished before running next test (i.e. clean slate)
    Base.metadata.drop_all(bind=engine)