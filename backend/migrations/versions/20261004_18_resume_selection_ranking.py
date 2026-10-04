"""resume selection ranking
Revision ID: 20261004_18
Revises: 20261004_17
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision='20261004_18';down_revision='20261004_17';branch_labels=None;depends_on=None
def upgrade():op.add_column('resume_selections',sa.Column('selection_score',sa.Integer,nullable=False,server_default='0'));op.add_column('resume_selections',sa.Column('selection_evidence',postgresql.JSONB,nullable=False,server_default='{}'))
def downgrade():op.drop_column('resume_selections','selection_evidence');op.drop_column('resume_selections','selection_score')
