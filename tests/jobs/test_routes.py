import pytest
from sqlalchemy.exc import IntegrityError

complete_job_data = {"name": "extraction-01", "status": "running", "source": "catchpoint", "description": "Extraction 1"}


class TestListJobs:
    def test_empty(self, client):
        response = client.get("/jobs/")

        assert response.status_code == 200
        assert response.get_json() == []

    def test_lists_only_active_jobs(self, client, job_factory):
        job = job_factory(name="active")
        job_factory(name="inactive", active=False)

        response = client.get("/jobs/")

        body = response.get_json()
        assert response.status_code == 200
        assert len(body) == 1
        assert body[0]["id"] == job.id
        assert body[0]["status"] == "running"


class TestCreateJob:
    def test_create(self, client):
        response = client.post("/jobs/", json=complete_job_data)

        body = response.get_json()
        assert response.status_code == 201
        assert body["id"] is not None
        for field, value in complete_job_data.items():
            assert body[field] == value

    @pytest.mark.parametrize("payload", [
        {"status": "running", "source": "catchpoint"},
        {"name": "extraction-01", "source": "catchpoint"},
        {**complete_job_data, "status": "pending"},
    ])
    def test_validation_error(self, client, payload):
        response = client.post("/jobs/", json=payload)

        assert response.status_code == 400
        assert response.get_json()["error"] == "validation_error"

    def test_unsupported_media_type(self, client):
        response = client.post("/jobs/", data="name=extraction-01")

        assert response.status_code == 415
        assert response.get_json()["error"] == "unsupported_media_type"

    def test_integrity_error(self, client, mocker):
        mocker.patch(
            "app.jobs.routes.job_service.create_job",
            side_effect=IntegrityError(None, None, Exception()),
        )

        response = client.post("/jobs/", json=complete_job_data)

        assert response.status_code == 400
        assert response.get_json()["error"] == "integrity_error"


class TestGetJob:
    def test_get(self, client, job_factory):
        job = job_factory()

        response = client.get(f"/jobs/{job.id}")

        assert response.status_code == 200
        assert response.get_json()["name"] == "extraction-01"

    def test_missing(self, client):
        response = client.get("/jobs/999")

        assert response.status_code == 404
        assert response.get_json()["error"] == "job_not_found"

    def test_soft_deleted(self, client, job_factory):
        job = job_factory(active=False)

        response = client.get(f"/jobs/{job.id}")

        assert response.status_code == 404


class TestReplaceJob:
    def test_replace(self, client, job_factory):
        job = job_factory()
        payload = {"name": "replaced", "status": "finished", "source": "other", "description": "new"}

        response = client.put(f"/jobs/{job.id}", json=payload)

        body = response.get_json()
        assert response.status_code == 200
        for field, value in payload.items():
            assert body[field] == value

    def test_missing_required_field(self, client, job_factory):
        job = job_factory()

        response = client.put(f"/jobs/{job.id}", json={"name": "replaced"})

        assert response.status_code == 400
        assert response.get_json()["error"] == "validation_error"

    def test_missing(self, client):
        response = client.put("/jobs/999", json=complete_job_data)

        assert response.status_code == 404


class TestUpdateJob:
    def test_partial_update(self, client, job_factory):
        job = job_factory()

        response = client.patch(f"/jobs/{job.id}", json={"status": "canceled"})

        body = response.get_json()
        assert response.status_code == 200
        assert body["status"] == "canceled"
        assert body["name"] == "extraction-01"
        assert body["source"] == "catchpoint"

    def test_invalid_status(self, client, job_factory):
        job = job_factory()

        response = client.patch(f"/jobs/{job.id}", json={"status": "pending"})

        assert response.status_code == 400

    def test_missing(self, client):
        response = client.patch("/jobs/999", json={"name": "updated"})

        assert response.status_code == 404


class TestDeleteJob:
    def test_delete(self, client, job_factory):
        job = job_factory()

        response = client.delete(f"/jobs/{job.id}")

        assert response.status_code == 200
        assert response.get_json()["id"] == job.id
        assert client.get(f"/jobs/{job.id}").status_code == 404

    def test_delete_twice(self, client, job_factory):
        job = job_factory()
        client.delete(f"/jobs/{job.id}")

        response = client.delete(f"/jobs/{job.id}")

        assert response.status_code == 404

    def test_method_not_allowed(self, client):
        response = client.delete("/jobs/")

        assert response.status_code == 405
        assert response.get_json()["error"] == "method_not_allowed"
