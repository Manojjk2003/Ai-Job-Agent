"""hiring source discovery
Revision ID: 20261004_10
Revises: 20261004_09
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision='20261004_10';down_revision='20261004_09';branch_labels=None;depends_on=None
def upgrade():
 op.create_table('hiring_sources',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('name',sa.String(255),nullable=False),sa.Column('normalized_name',sa.String(255),nullable=False),sa.Column('source_type',sa.String(50),nullable=False),sa.Column('base_url',sa.String(2048)),sa.Column('description',sa.Text),sa.Column('is_active',sa.Boolean,nullable=False),sa.Column('created_at',sa.DateTime(timezone=True),nullable=False),sa.Column('updated_at',sa.DateTime(timezone=True),nullable=False),sa.UniqueConstraint('normalized_name','source_type',name='uq_hiring_source_name_type'))
 op.create_index('ix_hiring_sources_normalized_name','hiring_sources',['normalized_name']);op.create_index('ix_hiring_sources_source_type','hiring_sources',['source_type'])
 op.create_table('company_hiring_sources',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('company_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('companies.id',ondelete='CASCADE'),nullable=False),sa.Column('hiring_source_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('hiring_sources.id',ondelete='CASCADE'),nullable=False),sa.Column('source_url',sa.String(2048),nullable=False),sa.Column('normalized_source_url',sa.String(2048),nullable=False),sa.Column('external_reference',sa.String(255)),sa.Column('status',sa.String(20),nullable=False),sa.Column('confidence',sa.String(20),nullable=False),sa.Column('discovery_method',sa.String(50),nullable=False),sa.Column('first_seen_at',sa.DateTime(timezone=True),nullable=False),sa.Column('last_verified_at',sa.DateTime(timezone=True)),sa.Column('last_checked_at',sa.DateTime(timezone=True)),sa.Column('notes',sa.Text),sa.Column('created_at',sa.DateTime(timezone=True),nullable=False),sa.Column('updated_at',sa.DateTime(timezone=True),nullable=False),sa.UniqueConstraint('company_id','hiring_source_id','normalized_source_url',name='uq_company_hiring_source_url'))
 op.create_index('ix_company_hiring_sources_company_id','company_hiring_sources',['company_id']);op.create_index('ix_company_hiring_sources_hiring_source_id','company_hiring_sources',['hiring_source_id']);op.create_index('ix_company_hiring_sources_normalized_source_url','company_hiring_sources',['normalized_source_url'])
def downgrade():op.drop_table('company_hiring_sources');op.drop_table('hiring_sources')
