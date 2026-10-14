import os

from flask import Flask

from app.jobs.routes import jobs_bp
from .extensions import db, migrate
from app.jobs.models import Job
from app.errors import register_error_handlers

def create_app(config=None):
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    if config:
        app.config.update(config)

    
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(jobs_bp)
    
    register_error_handlers(app)

    return app