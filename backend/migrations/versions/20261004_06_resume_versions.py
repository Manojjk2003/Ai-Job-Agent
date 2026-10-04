"""resume versions
Revision ID: 20261004_06
Revises: 20261004_05
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision='20261004_06';down_revision='20261004_05';branch_labels=depends_on=None
def upgrade():op.create_table('resume_versions',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('resume_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('resumes.id',ondelete='CASCADE'),nullable=False),sa.Column('version_number',sa.Integer,nullable=False),sa.Column('parse_status',sa.String(20),nullable=False),sa.Column('parser_name',sa.String(80)),sa.Column('parser_version',sa.String(80)),sa.Column('extracted_text',sa.Text),sa.Column('structured_sections',postgresql.JSONB),sa.Column('text_hash',sa.String(64)),sa.Column('error_message',sa.String(500)),sa.Column('created_at',sa.DateTime(timezone=True)),sa.Column('updated_at',sa.DateTime(timezone=True)),sa.Column('parsed_at',sa.DateTime(timezone=True)),sa.UniqueConstraint('resume_id','version_number',name='uq_resume_version_number'))
def downgrade():op.drop_table('resume_versions')
