"""tailored resume documents
Revision ID: 20261004_19
Revises: 20261004_18
"""
from alembic import op
import sqlalchemy as sa
revision='20261004_19';down_revision='20261004_18';branch_labels=None;depends_on=None
def upgrade():op.add_column('tailored_resumes',sa.Column('document_status',sa.String(30),nullable=False,server_default='pending'));op.add_column('tailored_resumes',sa.Column('document_storage_key',sa.String(500)))
def downgrade():op.drop_column('tailored_resumes','document_storage_key');op.drop_column('tailored_resumes','document_status')
