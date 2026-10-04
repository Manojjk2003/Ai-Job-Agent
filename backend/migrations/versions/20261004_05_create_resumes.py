"""create resumes
Revision ID: 20261004_05
Revises: 20261004_04
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision='20261004_05';down_revision='20261004_04';branch_labels=depends_on=None
def upgrade():
 op.create_table('resumes',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('candidate_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('candidates.id',ondelete='CASCADE'),nullable=False),sa.Column('original_filename',sa.String(255),nullable=False),sa.Column('storage_key',sa.String(500),nullable=False,unique=True),sa.Column('mime_type',sa.String(100),nullable=False),sa.Column('file_size',sa.Integer,nullable=False),sa.Column('file_hash',sa.String(64),nullable=False),sa.Column('status',sa.String(20),nullable=False),sa.Column('created_at',sa.DateTime(timezone=True)),sa.Column('updated_at',sa.DateTime(timezone=True)),sa.UniqueConstraint('candidate_id','file_hash',name='uq_candidate_resume_hash'));op.create_index('ix_resumes_candidate_id','resumes',['candidate_id'])
def downgrade():op.drop_index('ix_resumes_candidate_id',table_name='resumes');op.drop_table('resumes')
