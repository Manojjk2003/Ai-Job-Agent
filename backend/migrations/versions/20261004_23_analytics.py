"""candidate analytics recommendations
Revision ID: 20261004_23
Revises: 20261004_22
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision='20261004_23';down_revision='20261004_22';branch_labels=None;depends_on=None
def upgrade():
 op.create_table('recommendations',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('candidate_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('candidates.id',ondelete='CASCADE'),nullable=False),sa.Column('recommendation_type',sa.String(50),nullable=False),sa.Column('title',sa.String(255),nullable=False),sa.Column('description',sa.String(2000),nullable=False),sa.Column('evidence',postgresql.JSONB,nullable=False),sa.Column('priority',sa.String(20),nullable=False),sa.Column('confidence',sa.String(30),nullable=False),sa.Column('status',sa.String(20),nullable=False),sa.Column('generation_method',sa.String(30),nullable=False),sa.Column('created_at',sa.DateTime(timezone=True),nullable=False),sa.Column('updated_at',sa.DateTime(timezone=True),nullable=False));op.create_index('ix_recommendations_candidate_id','recommendations',['candidate_id'])
def downgrade():op.drop_table('recommendations')
