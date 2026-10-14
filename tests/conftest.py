import os

import pytest

from app import create_app
from app.extensions import db
from app.jobs.models import Job

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://postgres:p4$$w0rd@localhost/jobs_test",
)


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": TEST_DATABASE_URL,
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def job_factory(app):
    def make_job(**overrides):
        data = {
            "name": "extraction-01",
            "status": "running",
            "source": "catchpoint",
            "description": "Extraction 1",
            **overrides,
        }
        job = Job(**data)
        db.session.add(job)
        db.session.commit()
        return job

    return make_job
