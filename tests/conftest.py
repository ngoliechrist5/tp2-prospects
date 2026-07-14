import pytest
from app import create_app, db

@pytest.fixture
def app():
    test_config = {
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'TESTING': True,
        'SECRET_KEY': 'test-secret-key'
    }
    app = create_app(test_config)

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()