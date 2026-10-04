"""application preparation and tracking
Revision ID: 20261004_20
Revises: 20261004_19
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision='20261004_20';down_revision='20261004_19';branch_labels=None;depends_on=None
def upgrade():
 op.create_table('applications',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('candidate_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('candidates.id',ondelete='CASCADE'),nullable=False),sa.Column('job_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('jobs.id',ondelete='RESTRICT'),nullable=False),sa.Column('resume_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('resumes.id',ondelete='RESTRICT'),nullable=False),sa.Column('tailored_resume_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('tailored_resumes.id',ondelete='SET NULL')),sa.Column('application_url',sa.String(2048)),sa.Column('application_method',sa.String(30),nullable=False),sa.Column('application_source',sa.String(100),nullable=False),sa.Column('status',sa.String(30),nullable=False),sa.Column('notes',sa.Text),sa.Column('created_at',sa.DateTime(timezone=True),nullable=False),sa.Column('updated_at',sa.DateTime(timezone=True),nullable=False),sa.UniqueConstraint('candidate_id','job_id',name='uq_candidate_application_job'))
 op.create_table('application_events',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('application_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('applications.id',ondelete='CASCADE'),nullable=False),sa.Column('event_type',sa.String(50),nullable=False),sa.Column('from_status',sa.String(30)),sa.Column('to_status',sa.String(30)),sa.Column('note',sa.Text),sa.Column('metadata_json',postgresql.JSONB),sa.Column('created_at',sa.DateTime(timezone=True),nullable=False))
def downgrade():op.drop_table('application_events');op.drop_table('applications')
