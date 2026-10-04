"""candidate preferences
Revision ID: 20261004_08
Revises: 20261004_07
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision='20261004_08';down_revision='20261004_07';branch_labels=depends_on=None
def upgrade():
 op.create_table('candidate_preferences',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('candidate_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('candidates.id',ondelete='CASCADE'),nullable=False,unique=True),sa.Column('job_search_active',sa.Boolean,nullable=False),sa.Column('work_modes',sa.Text),sa.Column('employment_types',sa.Text),sa.Column('target_seniority',sa.Text),sa.Column('min_experience_years',sa.Integer),sa.Column('max_experience_years',sa.Integer),sa.Column('min_salary',sa.Integer),sa.Column('max_salary',sa.Integer),sa.Column('salary_currency',sa.String(10)),sa.Column('salary_period',sa.String(20)),sa.Column('relocation_preference',sa.String(20)),sa.Column('company_preferences',sa.Text),sa.Column('created_at',sa.DateTime(timezone=True)),sa.Column('updated_at',sa.DateTime(timezone=True)))
 op.create_table('candidate_preference_locations',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('candidate_preference_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('candidate_preferences.id',ondelete='CASCADE'),nullable=False),sa.Column('display_name',sa.String(255),nullable=False),sa.Column('normalized_name',sa.String(255),nullable=False),sa.Column('is_primary',sa.Boolean,nullable=False),sa.UniqueConstraint('candidate_preference_id','normalized_name',name='uq_preference_location'))
def downgrade():op.drop_table('candidate_preference_locations');op.drop_table('candidate_preferences')
