import pytest

from app.jobs.service import JobService
from app.errors import JobNotFoundError

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
    
        result = job_service.create_job(1)
        
        mock_repository.return_value.create.assert_called_once_with(1)
        assert result == expected_job
    
    def test_get_all_jobs(self, mocker): 
        mock_repository = mocker.patch("app.jobs.service.JobRepository")
        expected_jobs = mocker.Mock()
        mock_repository.return_value.get_all = expected_jobs
        
        job_service = JobService()
        
        result = job_service.get_all_jobs()
        mock_repository.return_value.get_all.return_value = expected_job
    
    def test_replace_job(self):
        pass
    
    def test_update_job(self):
        pass
    
    def test_delete_job(self):
        pass