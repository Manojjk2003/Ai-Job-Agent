"""company discovery foundation

Revision ID: 20261004_09
Revises: 20261004_08
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20261004_09"
down_revision = "20261004_08"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "companies",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("canonical_name", sa.String(255), nullable=False),
        sa.Column("normalized_name", sa.String(255), nullable=False),
        sa.Column("legal_name", sa.String(255)),
        sa.Column("website_url", sa.String(2048)),
        sa.Column("website_domain", sa.String(255)),
        sa.Column("linkedin_url", sa.String(2048)),
        sa.Column("description", sa.Text),
        sa.Column("industry", sa.String(255)),
        sa.Column("company_size", sa.String(100)),
        sa.Column("company_stage", sa.String(100)),
        sa.Column("logo_url", sa.String(2048)),
        sa.Column("headquarters_location_id", postgresql.UUID(as_uuid=True)),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("confidence", sa.String(20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("normalized_name"),
        sa.UniqueConstraint("website_domain"),
    )
    op.create_index("ix_companies_normalized_name", "companies", ["normalized_name"])
    op.create_index("ix_companies_website_domain", "companies", ["website_domain"])
    op.create_table(
        "company_locations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id", ondelete="CASCADE"), nullable=False),
        sa.Column("location_name", sa.String(255), nullable=False),
        sa.Column("normalized_location", sa.String(512), nullable=False),
        sa.Column("area", sa.String(255)), sa.Column("city", sa.String(255)), sa.Column("state", sa.String(255)), sa.Column("country", sa.String(255)), sa.Column("postal_code", sa.String(30)),
        sa.Column("latitude", sa.Float), sa.Column("longitude", sa.Float), sa.Column("location_type", sa.String(20), nullable=False),
        sa.Column("is_headquarters", sa.Boolean, nullable=False), sa.Column("is_verified", sa.Boolean, nullable=False), sa.Column("confidence", sa.String(20), nullable=False), sa.Column("source", sa.String(50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("company_id", "normalized_location", name="uq_company_location_normalized"),
    )
    op.create_index("ix_company_locations_company_id", "company_locations", ["company_id"])
    op.create_index("ix_company_locations_city", "company_locations", ["city"])
    op.create_foreign_key("fk_companies_headquarters_location", "companies", "company_locations", ["headquarters_location_id"], ["id"], ondelete="SET NULL")
    op.create_table(
        "company_discovery_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("candidate_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False),
        sa.Column("role_profile_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("role_profiles.id", ondelete="SET NULL")),
        sa.Column("query", sa.String(500)), sa.Column("location_name", sa.String(255), nullable=False), sa.Column("area", sa.String(255)), sa.Column("city", sa.String(255)), sa.Column("state", sa.String(255)), sa.Column("country", sa.String(255)),
        sa.Column("provider_name", sa.String(100), nullable=False), sa.Column("status", sa.String(20), nullable=False), sa.Column("result_count", sa.Integer, nullable=False), sa.Column("error_message", sa.Text), sa.Column("started_at", sa.DateTime(timezone=True)), sa.Column("completed_at", sa.DateTime(timezone=True)), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_company_discovery_runs_candidate_id", "company_discovery_runs", ["candidate_id"])
    op.create_table(
        "company_discovery_run_results",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("discovery_run_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("company_discovery_runs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id", ondelete="CASCADE"), nullable=False),
        sa.Column("provider_name", sa.String(100), nullable=False), sa.Column("provider_company_id", sa.String(255)), sa.Column("confidence", sa.String(20), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("discovery_run_id", "company_id", "provider_name", name="uq_discovery_run_company_provider"),
    )
    op.create_index("ix_company_discovery_run_results_discovery_run_id", "company_discovery_run_results", ["discovery_run_id"])
    op.create_index("ix_company_discovery_run_results_company_id", "company_discovery_run_results", ["company_id"])


def downgrade():
    op.drop_table("company_discovery_run_results")
    op.drop_table("company_discovery_runs")
    op.drop_constraint("fk_companies_headquarters_location", "companies", type_="foreignkey")
    op.drop_table("company_locations")
    op.drop_table("companies")
