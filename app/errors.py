from flask import jsonify
from marshmallow import ValidationError

class JobNotFoundError(Exception):
    pass

def register_error_handlers(app):
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({
            "error": "validation_error",
            "message" : "Invalid request Data.",
            "details" : error.messages
        }), 400
    
    @app.errorhandler(JobNotFoundError)
    def handle_job_not_found(error):
        return jsonify({
            "error": "job_not_found",
            "message" : "Job not Found."
        }), 404