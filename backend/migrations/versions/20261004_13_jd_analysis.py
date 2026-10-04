"""jd analysis
Revision ID: 20261004_13
Revises: 20261004_12
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision='20261004_13';down_revision='20261004_12';branch_labels=None;depends_on=None
def upgrade():
 op.create_table('job_analyses',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('job_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('jobs.id',ondelete='CASCADE'),nullable=False),sa.Column('status',sa.String(20),nullable=False),sa.Column('analysis_version',sa.String(30),nullable=False),sa.Column('model_provider',sa.String(50),nullable=False),sa.Column('model_name',sa.String(100)),sa.Column('prompt_version',sa.String(30),nullable=False),sa.Column('source_content_hash',sa.String(64),nullable=False),sa.Column('raw_response_hash',sa.String(64)),sa.Column('analyzed_at',sa.DateTime(timezone=True)),sa.Column('error_message',sa.Text),sa.Column('created_at',sa.DateTime(timezone=True),nullable=False),sa.Column('updated_at',sa.DateTime(timezone=True),nullable=False))
 op.create_table('job_requirements',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('analysis_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('job_analyses.id',ondelete='CASCADE'),nullable=False),sa.Column('job_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('jobs.id',ondelete='CASCADE'),nullable=False),sa.Column('requirement_type',sa.String(50),nullable=False),sa.Column('importance',sa.String(30),nullable=False),sa.Column('description',sa.Text,nullable=False),sa.Column('normalized_text',sa.Text,nullable=False),sa.Column('source_section',sa.String(100)),sa.Column('confidence',sa.String(20),nullable=False))
 op.create_table('job_skills',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('analysis_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('job_analyses.id',ondelete='CASCADE'),nullable=False),sa.Column('job_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('jobs.id',ondelete='CASCADE'),nullable=False),sa.Column('skill_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('skills.id',ondelete='RESTRICT'),nullable=False),sa.Column('importance',sa.String(30),nullable=False),sa.Column('evidence_text',sa.Text,nullable=False),sa.Column('confidence',sa.String(20),nullable=False),sa.Column('source_requirement_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('job_requirements.id',ondelete='SET NULL')),sa.UniqueConstraint('analysis_id','skill_id',name='uq_job_analysis_skill'))
def downgrade():op.drop_table('job_skills');op.drop_table('job_requirements');op.drop_table('job_analyses')
