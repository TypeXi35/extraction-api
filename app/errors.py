from flask import jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import UnsupportedMediaType, MethodNotAllowed

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
        
    @app.errorhandler(UnsupportedMediaType)
    def handle_unsupported_media_type(error):
        return jsonify({
            "error": "unsupported_media_type",
            "message": "Content-Type must be application/json."
        }), 415
    
    @app.errorhandler(MethodNotAllowed)
    def handle_method_not_allowed(error):
            return jsonify({
                "error": "method_not_allowed",
                "message" : "This HTTP method is not allowed for this resource."
            }), 405