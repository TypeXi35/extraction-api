from datetime import datetime, timezone

from app.extensions import db

class Job(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    status = db.Column(db.String(100), nullable = False)
    source = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(100), nullable = True)
    created_at = db.Column(db.DateTime, default =lambda: datetime.now(datetime.timezone.utc), nullable = False)
    updated_at = db.Column(
        db.DateTime,
        default =lambda: datetime.now(datetime.timezone.utc),
        onupdate =lambda: datetime.now(datetime.timezone.utc),
        nullable = False
    )
    active = db.Column(db.Boolean, default = True, nullable = False)