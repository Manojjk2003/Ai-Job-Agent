"""role profiles
Revision ID: 20261004_07
Revises: 20261004_06
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision='20261004_07';down_revision='20261004_06';branch_labels=depends_on=None
def upgrade():
 op.create_table('role_profiles',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('candidate_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('candidates.id',ondelete='CASCADE'),nullable=False),sa.Column('name',sa.String(255),nullable=False),sa.Column('target_designation',sa.String(255),nullable=False),sa.Column('headline',sa.String(255)),sa.Column('summary',sa.Text),sa.Column('target_seniority',sa.String(20)),sa.Column('is_default',sa.Boolean,nullable=False),sa.Column('is_active',sa.Boolean,nullable=False),sa.Column('created_at',sa.DateTime(timezone=True)),sa.Column('updated_at',sa.DateTime(timezone=True)));op.create_index('ix_role_profiles_candidate_id','role_profiles',['candidate_id'])
 op.create_table('role_profile_skills',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('role_profile_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('role_profiles.id',ondelete='CASCADE'),nullable=False),sa.Column('candidate_skill_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('candidate_skills.id',ondelete='CASCADE'),nullable=False),sa.Column('priority',sa.Integer,nullable=False),sa.Column('is_primary',sa.Boolean,nullable=False),sa.Column('created_at',sa.DateTime(timezone=True)),sa.UniqueConstraint('role_profile_id','candidate_skill_id',name='uq_role_profile_skill'))
 for table,column,target,name in [('role_profile_experiences','experience_id','experiences.id','uq_role_profile_experience'),('role_profile_projects','project_id','projects.id','uq_role_profile_project')]:op.create_table(table,sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('role_profile_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('role_profiles.id',ondelete='CASCADE'),nullable=False),sa.Column(column,postgresql.UUID(as_uuid=True),sa.ForeignKey(target,ondelete='CASCADE'),nullable=False),sa.Column('priority',sa.Integer,nullable=False),sa.Column('is_primary',sa.Boolean,nullable=False),sa.Column('created_at',sa.DateTime(timezone=True)),sa.UniqueConstraint('role_profile_id',column,name=name))
def downgrade():op.drop_table('role_profile_projects');op.drop_table('role_profile_experiences');op.drop_table('role_profile_skills');op.drop_index('ix_role_profiles_candidate_id',table_name='role_profiles');op.drop_table('role_profiles')
