"""job normalization metadata
Revision ID: 20261004_12
Revises: 20261004_11
"""
from alembic import op
import sqlalchemy as sa
revision='20261004_12';down_revision='20261004_11';branch_labels=None;depends_on=None
def upgrade():
 op.add_column('jobs',sa.Column('normalization_version',sa.String(30)));op.add_column('jobs',sa.Column('normalized_at',sa.DateTime(timezone=True)));op.add_column('job_sources',sa.Column('normalization_status',sa.String(30),nullable=False,server_default='pending'));op.add_column('job_sources',sa.Column('normalization_version',sa.String(30)));op.add_column('job_sources',sa.Column('normalization_error',sa.Text));op.add_column('job_sources',sa.Column('normalized_at',sa.DateTime(timezone=True)))
def downgrade():op.drop_column('job_sources','normalized_at');op.drop_column('job_sources','normalization_error');op.drop_column('job_sources','normalization_version');op.drop_column('job_sources','normalization_status');op.drop_column('jobs','normalized_at');op.drop_column('jobs','normalization_version')
