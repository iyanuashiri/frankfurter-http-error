import os
from fastapi.testclient import TestClient
import pytest

from app.core.database import Base
from app.main import app
from app.api.deps import get_db

from tests.database import engine
from tests.database import TestingSessionLocal


client = TestClient(app)


# def get_client():
#     return client

    
@pytest.fixture
def client():
    return TestClient(app)


# @pytest.fixture(autouse=True)
# def reset_database():

#     if os.path.exists("test.db"):
#         os.remove("test.db")

#     Base.metadata.create_all(bind=engine)

#     yield

#     engine.dispose()

#     if os.path.exists("test.db"):
#         os.remove("test.db")


@pytest.fixture(autouse=True)
def reset_database():

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    db = TestingSessionLocal()
    yield db
    db.close()

def override_get_db():

    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db