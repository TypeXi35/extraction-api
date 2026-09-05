from flask import Blueprint, jsonify, request

from app.jobs.service import JobService
from app.jobs.schemas import JobResponseSchema
from app.jobs.schemas import JobCreateSchema
from app.jobs.schemas import JobReplaceSchema
from app.jobs.schemas import JobUpdateSchema

job_service = JobService()
job_response_schema = JobResponseSchema()
job_create_schema = JobCreateSchema()
job_replace_schema = JobReplaceSchema()
job_update_schema = JobUpdateSchema()
multiple_jobs_response_schema = JobResponseSchema(many=True)

jobs_bp = Blueprint(
    "jobs",
    __name__,
    url_prefix="/jobs"
)

@jobs_bp.get("/")
def list_jobs():
    """
    Lists all Jobs registered
        Parameters:
            None
        Returns:
            JSON with list of jobs and status Code
    """
    job_list = job_service.get_all_jobs()
    return jsonify(multiple_jobs_response_schema.dump(job_list)), 200

@jobs_bp.post("/")
def create_job():
    """
    Creaets a new Job
        Parameters:
            Job data, to be defined
        Returns:
            JSON with the new Job created and status code
    """
    job_data = job_create_schema.load(request.json)
    job = job_service.create_job(job_data)
    
    return jsonify(job_response_schema.dump(job)), 201

@jobs_bp.get("/<int:job_id>")
def get_job_by_id(job_id):
    """
    Gets a job by its Id
        Parameters:
            job_id: ID of the job to retrieve
        Returns:
            JSON with the requested job
    """
    job = job_service.get_job(job_id)
    
    return jsonify(job_response_schema.dump(job)), 200

@jobs_bp.put("/<int:job_id>")
def replace_job(job_id):
    """
    Replaces a job with a new job data
        Parameters:
            job_id: the id of the job to be replaced
            replacement_job: the job to replace the old one
        
    """
    job_data = job_replace_schema.load(request.json)
    replaced_job = job_service.replace_job(job_id, job_data)
    
    return jsonify(job_response_schema.dump(replaced_job)), 200


@jobs_bp.patch("/<int:job_id>")
def update_job(job_id):
    """
    Updates the data of an existing job
        Parameters:
            job_id: the id of the job to be replaced
            job_data: the data to be replaced field by field i think, might check
        Returns:
            JSON with the updated job and HTTP status code
    """
    job_data = job_update_schema.load(request.json)
    updated_job = job_service.update_job(job_id, job_data)
    
    return jsonify(job_response_schema.dump(updated_job)), 200

@jobs_bp.delete("/<int:job_id>")
def delete_job(job_id):
    """
    'Deletes' a job (sets their inactive field to true)
        Parameters:
            job_id: id of job to delete
        Returns:
            ID of erased element, and message confirming the delete
    """
    deleted_job = job_service.delete_job(job_id)
    return jsonify(job_response_schema.dump(deleted_job)), 200