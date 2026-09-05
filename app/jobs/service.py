from app.jobs.repository import JobRepository
from app.jobs.models import Job
from app.errors import JobNotFoundError

class JobService:
    def __init__(self):
        self.job_repository = JobRepository()
        
    def get_job(self, job_id):
        job = self.job_repository.get_by_id(job_id)
        
        if job is None:
            raise JobNotFoundError(job_id)
        
        return job
    
    def create_job(self, job_data):
        job = Job(**job_data)
        self.job_repository.create(job)
        return job

    def get_all_jobs(self):
        return self.job_repository.get_all()
    
    def replace_job(self, job_id, job_data):
        job = self.job_repository.update(job_id, job_data)
        
        if job is None:
           raise JobNotFoundError(job_id)
        return job
    
    def update_job(self, job_id, job_data):
       job = self.job_repository.update(job_id, job_data)
       
       if job is None:
           raise JobNotFoundError(job_id)
       return job
        
    def delete_job(self, job_id):
        job = self.job_repository.delete(job_id)
        
        if job is None:
            raise JobNotFoundError(job_id)
        return job