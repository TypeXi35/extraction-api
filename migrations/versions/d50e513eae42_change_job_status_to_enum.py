"""change job status to enum

Revision ID: d50e513eae42
Revises: 67dcaa650037
Create Date: 2026-09-03 13:15:29.524473

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd50e513eae42'
down_revision = '67dcaa650037'
branch_labels = None
depends_on = None

def upgrade():
    job_status = sa.Enum(
        "running",
        "finished",
        "canceled",
        name="jobstatus"
    )

    job_status.create(op.get_bind(), checkfirst=True)

    op.alter_column(
        "job",
        "status",
        existing_type=sa.VARCHAR(length=100),
        type_=job_status,
        existing_nullable=False,
        postgresql_using="status::jobstatus",
    )


def downgrade():
    job_status = sa.Enum(
        "running",
        "finished",
        "canceled",
        name="jobstatus"
    )

    op.alter_column(
        "job",
        "status",
        existing_type=job_status,
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )

    job_status.drop(op.get_bind(), checkfirst=True)