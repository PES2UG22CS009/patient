"""create aaryan_singh tables

Revision ID: 111e9f3c230a
Revises:
Create Date: 2026-01-30 17:07:51.374000
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "111e9f3c230a"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1) Patients
    op.create_table(
        "aaryan_singh_patients",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("email", name="uq_aaryan_singh_patients_email"),
    )
    op.create_index(
        "ix_aaryan_singh_patients_email",
        "aaryan_singh_patients",
        ["email"],
        unique=True,
    )

    # 2) Doctors
    op.create_table(
        "aaryan_singh_doctors",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("full_name", sa.String(length=150), nullable=False),
        sa.Column("specialization", sa.String(length=100), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # 3) Appointments
    op.create_table(
        "aaryan_singh_appointments",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("doctor_id", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("duration_minutes", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["patient_id"],
            ["aaryan_singh_patients.id"],
            name="fk_aaryan_singh_appointments_patient_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["doctor_id"],
            ["aaryan_singh_doctors.id"],
            name="fk_aaryan_singh_appointments_doctor_id",
            ondelete="RESTRICT",
        ),
    )
    op.create_index(
        "idx_aaryan_singh_doctor_start_time",
        "aaryan_singh_appointments",
        ["doctor_id", "start_time"],
        unique=False,
    )
    op.create_index(
        "ix_aaryan_singh_appointments_start_time",
        "aaryan_singh_appointments",
        ["start_time"],
        unique=False,
    )


def downgrade() -> None:
    # Drop in reverse order
    op.drop_index("ix_aaryan_singh_appointments_start_time", table_name="aaryan_singh_appointments")
    op.drop_index("idx_aaryan_singh_doctor_start_time", table_name="aaryan_singh_appointments")
    op.drop_table("aaryan_singh_appointments")

    op.drop_table("aaryan_singh_doctors")

    op.drop_index("ix_aaryan_singh_patients_email", table_name="aaryan_singh_patients")
    op.drop_table("aaryan_singh_patients")
