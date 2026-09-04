from app.extensions import db
from app.jobs.models import Job
from sqlalchemy import select
from datetime import datetime, timezone

def get_current_time():
    return datetime.now(timezone.utc);

class JobRepository:
    def create(self, job: Job):
        db.session.add(job)
        db.session.commit()
        return job
    def get_by_id(self,job_id):
        job = db.session.get(Job, job_id)
        return job
    def get_all(self):
        statement = select(Job)
        result = db.session.execute(statement)
        return result.scalars().all()        
    def delete_job(self, job_id):
        job = db.session.get(Job,job_id);
        if job is None:
            return None
        job.active = False
        job.updated_at = get_current_time()
        db.session.commit()
        
        return job
    def replace_job(self, job):
        existing_job = db.session.get(Job, job.id)
        if existing_job is None:
            return None
        existing_job.name = job.name
        existing_job.status = job.status
        existing_job.source = job.source
        existing_job.description = job.description
        existing_job.updated_at = get_current_time()
        
        db.session.commit()
        
        
    def update_job(self, job_id, job_data):
        job = db.session.get(Job, job_id)
        if job is None:
            return None
        for field, value in job_data.items():
            setattr(job, field, value)
        
        job.updated_at = get_current_time();
        
        db.session.commit()
        
        return job