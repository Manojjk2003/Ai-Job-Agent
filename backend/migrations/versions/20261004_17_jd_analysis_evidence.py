"""jd analysis evidence
Revision ID: 20261004_17
Revises: 20261004_16
"""
from alembic import op
import sqlalchemy as sa
revision='20261004_17';down_revision='20261004_16';branch_labels=None;depends_on=None
def upgrade():op.add_column('job_requirements',sa.Column('evidence_text',sa.Text))
def downgrade():op.drop_column('job_requirements','evidence_text')
