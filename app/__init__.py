import os

from flask import Flask

from app.jobs.routes import jobs_bp
from .extensions import db, migrate
from app.jobs.models import Job
from app.errors import JobNotFoundError

def create_app():
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

    
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(jobs_bp)
    
    @app.errorhandler(JobNotFoundError)
    def handle_job_found(error):
        return {"error": "Job not found"}, 404

    return app