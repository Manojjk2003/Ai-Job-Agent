"""resume tailoring
Revision ID: 20261004_16
Revises: 20261004_15
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision='20261004_16';down_revision='20261004_15';branch_labels=None;depends_on=None
def upgrade():
 op.create_table('tailored_resumes',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('candidate_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('candidates.id',ondelete='CASCADE'),nullable=False),sa.Column('job_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('jobs.id',ondelete='CASCADE'),nullable=False),sa.Column('resume_selection_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('resume_selections.id',ondelete='RESTRICT'),nullable=False),sa.Column('status',sa.String(30),nullable=False),sa.Column('generation_version',sa.Integer,nullable=False),sa.Column('template_version',sa.String(30),nullable=False),sa.Column('source_hash',sa.String(64),nullable=False),sa.Column('structured_content',postgresql.JSONB,nullable=False),sa.Column('validation_summary',postgresql.JSONB,nullable=False),sa.Column('approved_at',sa.DateTime(timezone=True)),sa.Column('rejected_at',sa.DateTime(timezone=True)),sa.Column('rejection_reason',sa.Text),sa.Column('created_at',sa.DateTime(timezone=True),nullable=False))
 op.create_table('tailored_resume_claims',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('tailored_resume_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('tailored_resumes.id',ondelete='CASCADE'),nullable=False),sa.Column('claim_text',sa.Text,nullable=False),sa.Column('source_type',sa.String(30),nullable=False),sa.Column('source_id',postgresql.UUID(as_uuid=True)),sa.Column('created_at',sa.DateTime(timezone=True),nullable=False))
def downgrade():op.drop_table('tailored_resume_claims');op.drop_table('tailored_resumes')
