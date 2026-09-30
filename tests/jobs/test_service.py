import pytest

from app.jobs.service import JobService
from app.errors import JobNotFoundError
from app.jobs.models import Job

complete_job_data = {"name": "extraction-01","status":"running", "source":"catchpoint", "description": "Extraction 1"}
job_data_no_description = {"name": "extraction-01","status":"running", "source":"catchpoint"}

class TestJobService:
    def test_get_job(self, mocker):
        mock_repository = mocker.patch("app.jobs.service.JobRepository")
        expected_job = mocker.Mock()
        mock_repository.return_value.get_by_id.return_value = expected_job
        
        job_service = JobService()
    
        result = job_service.get_job(1)
        
        mock_repository.return_value.get_by_id.assert_called_once_with(1)
        assert result == expected_job
        
    def test_create_job(self, mocker):
        mock_repository = mocker.patch("app.jobs.service.JobRepository")
        expected_job = mocker.Mock()
        mock_repository.return_value.create.return_value = expected_job
        
        job_service = JobService()
        
        result = job_service.create_job(complete_job_data)
    
        mock_repository.return_value.create.assert_called_once()

        job_argument = mock_repository.return_value.create.call_args.args[0]

        assert isinstance(job_argument, Job)
        assert job_argument.name == complete_job_data["name"]
        assert job_argument.status == complete_job_data["status"]
        assert job_argument.source == complete_job_data["source"]
        assert job_argument.description == complete_job_data["description"]
        
        assert result == expected_job
    
    def test_get_all_jobs(self, mocker): 
        mock_repository = mocker.patch("app.jobs.service.JobRepository")
        expected_jobs = mocker.Mock()
        mock_repository.return_value.get_all.return_value = expected_jobs
        
        job_service = JobService()
        
        result = job_service.get_all_jobs()
        assert result == expected_jobs
    
    def test_replace_job(self, mocker):
        mock_repository = mocker.patch("app.jobs.service.JobRepository")
        expected_job = mocker.Mock()
        mock_repository.return_value.update.return_value = expected_job
        
        job_service = JobService()
    
        result = job_service.replace_job(1,complete_job_data)
        
        mock_repository.return_value.update.assert_called_once_with(1,complete_job_data)
        assert result == expected_job
    
    def test_update_job(self, mocker):
        mock_repository = mocker.patch("app.jobs.service.JobRepository")
        expected_job = mocker.Mock()
        mock_repository.return_value.update.return_value = expected_job
        
        job_service = JobService()
    
        result = job_service.update_job(1,complete_job_data)
        
        mock_repository.return_value.update.assert_called_once_with(1, complete_job_data)
        assert result == expected_job
    
    def test_delete_job(self, mocker):
        mock_repository = mocker.patch("app.jobs.service.JobRepository")
        expected_job = mocker.Mock()
        mock_repository.return_value.delete.return_value = expected_job
        
        job_service = JobService()
    
        result = job_service.delete_job(1)
        
        mock_repository.return_value.delete.assert_called_once_with(1)
        assert result == expected_job