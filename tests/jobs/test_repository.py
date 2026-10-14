import pytest
from sqlalchemy.exc import IntegrityError

from app.jobs.models import Job, JobStatus
from app.jobs.repository import JobRepository


@pytest.fixture
def repository():
    return JobRepository()


class TestJobRepository:
    def test_create(self, app, repository):
        job = Job(name="extraction-01", status="running", source="catchpoint")

        result = repository.create(job)

        assert result.id is not None
        assert result.status == JobStatus.RUNNING
        assert result.active is True
        assert result.created_at is not None
        assert result.updated_at is not None

    def test_create_integrity_error_rolls_back(self, app, repository):
        job = Job(name=None, status="running", source="catchpoint")

        with pytest.raises(IntegrityError):
            repository.create(job)

        # Session is still usable after the rollback
        assert repository.get_all() == []

    def test_get_by_id(self, repository, job_factory):
        job = job_factory()

        assert repository.get_by_id(job.id) == job

    def test_get_by_id_missing(self, app, repository):
        assert repository.get_by_id(999) is None

    def test_get_by_id_inactive(self, repository, job_factory):
        job = job_factory(active=False)

        assert repository.get_by_id(job.id) is None

    def test_get_all_returns_only_active(self, repository, job_factory):
        active_job = job_factory(name="active")
        job_factory(name="inactive", active=False)

        assert repository.get_all() == [active_job]

    def test_delete(self, repository, job_factory):
        job = job_factory()
        previous_updated_at = job.updated_at

        result = repository.delete(job.id)

        assert result.active is False
        assert result.updated_at > previous_updated_at
        assert repository.get_by_id(job.id) is None

    def test_delete_missing(self, app, repository):
        assert repository.delete(999) is None

    def test_delete_already_deleted(self, repository, job_factory):
        job = job_factory()
        repository.delete(job.id)

        assert repository.delete(job.id) is None

    def test_update(self, repository, job_factory):
        job = job_factory()
        previous_updated_at = job.updated_at

        result = repository.update(job.id, {"name": "updated", "status": "finished"})

        assert result.name == "updated"
        assert result.status == JobStatus.FINISHED
        assert result.source == "catchpoint"
        assert result.description == "Extraction 1"
        assert result.updated_at > previous_updated_at

    def test_update_missing(self, app, repository):
        assert repository.update(999, {"name": "updated"}) is None
