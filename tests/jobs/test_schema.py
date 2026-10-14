import pytest
from marshmallow import ValidationError

from app.jobs.schemas import (
    JobCreateSchema,
    JobResponseSchema,
    JobReplaceSchema,
    JobUpdateSchema,
)
from app.jobs.models import JobStatus


@pytest.fixture
def valid_job_data():
    return {
        "name": "Test job",
        "status": "running",
        "source": "test-source",
        "description": "Test description",
    }


@pytest.fixture
def valid_job_data_without_description():
    return {
        "name": "Test job",
        "status": "running",
        "source": "test-source",
    }


class TestJobCreateSchema:

    def test_valid_data(self, valid_job_data):
        result = JobCreateSchema().load(valid_job_data)

        assert result == valid_job_data

    def test_required_fields(self):
        with pytest.raises(ValidationError):
            JobCreateSchema().load({})

    @pytest.mark.parametrize("status", [
        "invalid",
        "pending",
        "completed",
        "",
    ])
    def test_invalid_status(self, valid_job_data_without_description, status):
        data = {
            **valid_job_data_without_description,
            "status": status,
        }

        with pytest.raises(ValidationError):
            JobCreateSchema().load(data)

    @pytest.mark.parametrize("status", [
        "running",
        "finished",
        "canceled",
    ])
    def test_valid_status(self, valid_job_data_without_description, status):
        data = {
            **valid_job_data_without_description,
            "status": status,
        }

        result = JobCreateSchema().load(data)

        assert result["status"] == status

    def test_description_can_be_none(self, valid_job_data):
        data = {
            **valid_job_data,
            "description": None,
        }

        result = JobCreateSchema().load(data)

        assert result["description"] is None


class TestJobReplaceSchema:

    def test_valid_data(self, valid_job_data):
        result = JobReplaceSchema().load(valid_job_data)

        assert result == valid_job_data

    def test_required_fields(self):
        with pytest.raises(ValidationError):
            JobReplaceSchema().load({})

    @pytest.mark.parametrize("status", [
        "invalid",
        "pending",
        "completed",
        "",
    ])
    def test_invalid_status(self, valid_job_data_without_description, status):
        data = {
            **valid_job_data_without_description,
            "status": status,
        }

        with pytest.raises(ValidationError):
            JobReplaceSchema().load(data)


class TestJobUpdateSchema:

    def test_empty_data_is_valid(self):
        result = JobUpdateSchema().load({})

        assert result == {}

    def test_partial_update(self):
        data = {
            "name": "Updated job",
        }

        result = JobUpdateSchema().load(data)

        assert result == data

    @pytest.mark.parametrize("status", [
        "invalid",
        "pending",
        "completed",
        "",
    ])
    def test_invalid_status(self, status):
        with pytest.raises(ValidationError):
            JobUpdateSchema().load({"status": status})

    @pytest.mark.parametrize("status", [
        "running",
        "finished",
        "canceled",
    ])
    def test_valid_status(self, status):
        result = JobUpdateSchema().load({"status": status})

        assert result["status"] == status


class TestJobResponseSchema:

    def test_valid_response(self, valid_job_data):
        data = {
            "id": 1,
            **valid_job_data,
        }

        result = JobResponseSchema().load(data)

        assert result["id"] == 1
        assert result["name"] == "Test job"
        assert result["status"] == JobStatus.RUNNING
        assert result["source"] == "test-source"
        assert result["description"] == "Test description"

    def test_description_can_be_none(self, valid_job_data):
        data = {
            "id": 1,
            **valid_job_data,
            "description": None,
        }

        result = JobResponseSchema().load(data)

        assert result["description"] is None