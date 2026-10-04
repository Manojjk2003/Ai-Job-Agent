"""create skills domain
Revision ID: 20261004_04
Revises: 20261004_03
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision='20261004_04'; down_revision='20261004_03'; branch_labels=depends_on=None
def upgrade():
 op.create_table('skills',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('name',sa.String(255),nullable=False),sa.Column('normalized_name',sa.String(255),nullable=False,unique=True),sa.Column('description',sa.Text),sa.Column('category',sa.String(80),nullable=False),sa.Column('is_active',sa.Boolean,nullable=False),sa.Column('created_at',sa.DateTime(timezone=True)),sa.Column('updated_at',sa.DateTime(timezone=True)));op.create_index('ix_skills_normalized_name','skills',['normalized_name'])
 op.create_table('skill_aliases',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('skill_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('skills.id',ondelete='CASCADE'),nullable=False),sa.Column('alias',sa.String(255),nullable=False),sa.Column('normalized_alias',sa.String(255),nullable=False,unique=True),sa.Column('created_at',sa.DateTime(timezone=True)));op.create_index('ix_skill_aliases_normalized_alias','skill_aliases',['normalized_alias'])
 op.create_table('candidate_skills',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('candidate_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('candidates.id',ondelete='CASCADE'),nullable=False),sa.Column('skill_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('skills.id',ondelete='RESTRICT'),nullable=False),sa.Column('proficiency',sa.String(20)),sa.Column('years_experience',sa.Integer),sa.Column('is_primary',sa.Boolean,nullable=False),sa.Column('created_at',sa.DateTime(timezone=True)),sa.Column('updated_at',sa.DateTime(timezone=True)),sa.UniqueConstraint('candidate_id','skill_id',name='uq_candidate_skill'))
 op.create_table('skill_evidence',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('candidate_skill_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('candidate_skills.id',ondelete='CASCADE'),nullable=False),sa.Column('evidence_type',sa.String(30),nullable=False),sa.Column('reference_id',postgresql.UUID(as_uuid=True)),sa.Column('description',sa.Text),sa.Column('created_at',sa.DateTime(timezone=True)))
def downgrade():
 op.drop_table('skill_evidence');op.drop_table('candidate_skills');op.drop_index('ix_skill_aliases_normalized_alias',table_name='skill_aliases');op.drop_table('skill_aliases');op.drop_index('ix_skills_normalized_name',table_name='skills');op.drop_table('skills')
