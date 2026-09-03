from flask import Blueprint

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
    return {"message": "List jobs lives!"}, 200


@jobs_bp.post("/")
def create_job():
    """
    Creaets a new Job
        Parameters:
            Job data, to be defined
        Returns:
            JSON with the new Job created and status code
    """
    return {"message": "Create Jobs lives!"}, 201

@jobs_bp.get("/<int:job_id>")
def get_job_by_id(job_id):
    """
    Gets a job by its Id
        Parameters:
            job_id
        Returns:
            JSON with the specified job
    """
    return {"message": "Get job by id lives!"}, 200

@jobs_bp.put("/<int:job_id>")
def replace_job(job_id):
    """
    Replaces a job with a new job data
        Parameters:
            job_id: the id of the job to be replaced
            replacement_job: the job to replace the old one
        
    """
    return {"message": "Replace job Lives!"}, 200


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
    return {"message": "Update job Lives!"}, 200

@jobs_bp.delete("/<int:job_id>")
def delete_job(job_id):
    """
    'Deletes' a job (sets their inactive field to true)
        Parameters:
            job_id: id of job to delete
        Returns:
            ID of erased element, and message confirming the delete
    """
    return {"message": "Delete Job Lives!"}, 200