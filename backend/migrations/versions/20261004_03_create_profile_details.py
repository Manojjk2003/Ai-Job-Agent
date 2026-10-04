"""create candidate profile detail tables

Revision ID: 20261004_03
Revises: 20261004_02
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision = "20261004_03"
down_revision = "20261004_02"
branch_labels = depends_on = None

def _audit(columns):
    columns.extend([sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False)])
def upgrade():
    exp=[sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),sa.Column("candidate_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False),sa.Column("company_name",sa.String(255),nullable=False),sa.Column("job_title",sa.String(255),nullable=False),sa.Column("employment_type",sa.String(80)),sa.Column("location",sa.String(255)),sa.Column("start_date",sa.Date,nullable=False),sa.Column("end_date",sa.Date),sa.Column("is_current",sa.Boolean,nullable=False),sa.Column("description",sa.Text),sa.Column("display_order",sa.Integer,nullable=False)] ; _audit(exp); op.create_table("experiences",*exp); op.create_index("ix_experiences_candidate_id","experiences",["candidate_id"])
    ach=[sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True),sa.Column("experience_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("experiences.id",ondelete="CASCADE"),nullable=False),sa.Column("achievement",sa.Text,nullable=False),sa.Column("display_order",sa.Integer,nullable=False)] ; _audit(ach); op.create_table("experience_achievements",*ach); op.create_index("ix_experience_achievements_experience_id","experience_achievements",["experience_id"])
    edu=[sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True),sa.Column("candidate_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("candidates.id",ondelete="CASCADE"),nullable=False),sa.Column("institution",sa.String(255),nullable=False),sa.Column("degree",sa.String(255)),sa.Column("field_of_study",sa.String(255)),sa.Column("start_date",sa.Date),sa.Column("end_date",sa.Date),sa.Column("grade",sa.String(100)),sa.Column("description",sa.Text),sa.Column("display_order",sa.Integer,nullable=False)] ; _audit(edu); op.create_table("education",*edu); op.create_index("ix_education_candidate_id","education",["candidate_id"])
    project=[sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True),sa.Column("candidate_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("candidates.id",ondelete="CASCADE"),nullable=False),sa.Column("name",sa.String(255),nullable=False),sa.Column("description",sa.Text),sa.Column("role",sa.String(255)),sa.Column("project_type",sa.String(100)),sa.Column("start_date",sa.Date),sa.Column("end_date",sa.Date),sa.Column("project_url",sa.String(500)),sa.Column("repository_url",sa.String(500)),sa.Column("display_order",sa.Integer,nullable=False)] ; _audit(project); op.create_table("projects",*project); op.create_index("ix_projects_candidate_id","projects",["candidate_id"])
def downgrade():
    for table,index in [("projects","ix_projects_candidate_id"),("education","ix_education_candidate_id"),("experience_achievements","ix_experience_achievements_experience_id"),("experiences","ix_experiences_candidate_id")]: op.drop_index(index,table_name=table);op.drop_table(table)
