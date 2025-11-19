import pytest
from app import create_app
from app.models import db

@pytest.fixture(scope='module')
def test_client():
    app = create_app(testing=True)
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield client

    ctx.pop()

@pytest.fixture(scope='module')
def init_database():
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()