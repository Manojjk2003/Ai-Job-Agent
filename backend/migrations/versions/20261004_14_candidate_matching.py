"""candidate matching
Revision ID: 20261004_14
Revises: 20261004_13
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision='20261004_14';down_revision='20261004_13';branch_labels=None;depends_on=None
def upgrade():
 op.create_table('candidate_job_matches',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('candidate_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('candidates.id',ondelete='CASCADE'),nullable=False),sa.Column('job_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('jobs.id',ondelete='CASCADE'),nullable=False),sa.Column('role_profile_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('role_profiles.id',ondelete='SET NULL')),sa.Column('status',sa.String(20),nullable=False),sa.Column('match_version',sa.String(30),nullable=False),sa.Column('created_at',sa.DateTime(timezone=True),nullable=False),sa.Column('updated_at',sa.DateTime(timezone=True),nullable=False),sa.UniqueConstraint('candidate_id','job_id',name='uq_candidate_job_match'))
 op.create_table('candidate_job_match_evidence',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('match_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('candidate_job_matches.id',ondelete='CASCADE'),nullable=False),sa.Column('job_requirement_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('job_requirements.id',ondelete='SET NULL')),sa.Column('candidate_skill_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('candidate_skills.id',ondelete='SET NULL')),sa.Column('classification',sa.String(30),nullable=False),sa.Column('reason',sa.Text,nullable=False),sa.Column('created_at',sa.DateTime(timezone=True),nullable=False))
def downgrade():op.drop_table('candidate_job_match_evidence');op.drop_table('candidate_job_matches')
