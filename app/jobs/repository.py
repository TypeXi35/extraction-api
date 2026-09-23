from app.extensions import db
from app.jobs.models import Job
from sqlalchemy import select
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError

def get_current_time():
    return datetime.now(timezone.utc);
    
class JobRepository:
    def create(self, job: Job):
        db.session.add(job)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise
        return job
    
    def get_by_id(self,job_id):
        statement = select(Job).where(
            Job.id == job_id,
            Job.active.is_(True)
        )
        return db.session.execute(statement).scalar_one_or_none()
    
    def get_all(self):
        statement = select(Job).where(Job.active.is_(True))
        result = db.session.execute(statement)
        return result.scalars().all()        
    
    def delete(self, job_id):
        job = self.get_by_id(job_id)
        
        if job is None:
            return None
        
        job.active = False
        job.updated_at = get_current_time()
        
        db.session.commit()
        return job
    
        
    def update(self, job_id, job_data):
        job = self.get_by_id(job_id)
        
        if job is None:
            return None
        for field, value in job_data.items():
            setattr(job, field, value)
        
        job.updated_at = get_current_time();
        
        db.session.commit()
        
        return job
