from datetime import datetime, timezone

from app.extensions import db

from enum import Enum


class JobStatus(Enum):
    RUNNING = "running"
    FINISHED = "finished"
    CANCELED = "canceled"

class Job(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    status = db.Column(db.Enum(JobStatus, values_callable= lambda enum: [item.value for item in enum]), nullable = False)
    source = db.Column(db.String(100), nullable = False)
    description = db.Column(db.Text, nullable = True)
    created_at = db.Column(db.DateTime, default =lambda: datetime.now(timezone.utc), nullable = False)
    updated_at = db.Column(
        db.DateTime,
        default =lambda: datetime.now(timezone.utc),
        onupdate =lambda: datetime.now(timezone.utc),
        nullable = False
    )
    active = db.Column(db.Boolean, default = True, nullable = False)