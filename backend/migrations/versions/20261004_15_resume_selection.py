"""resume selection
Revision ID: 20261004_15
Revises: 20261004_14
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision='20261004_15';down_revision='20261004_14';branch_labels=None;depends_on=None
def upgrade():op.create_table('resume_selections',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('candidate_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('candidates.id',ondelete='CASCADE'),nullable=False),sa.Column('job_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('jobs.id',ondelete='CASCADE'),nullable=False),sa.Column('resume_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('resumes.id',ondelete='RESTRICT'),nullable=False),sa.Column('resume_version_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('resume_versions.id',ondelete='SET NULL')),sa.Column('role_profile_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('role_profiles.id',ondelete='SET NULL')),sa.Column('selection_method',sa.String(30),nullable=False),sa.Column('explanation',sa.Text,nullable=False),sa.Column('status',sa.String(20),nullable=False),sa.Column('created_at',sa.DateTime(timezone=True),nullable=False),sa.Column('updated_at',sa.DateTime(timezone=True),nullable=False),sa.UniqueConstraint('candidate_id','job_id',name='uq_resume_selection'))
def downgrade():op.drop_table('resume_selections')
