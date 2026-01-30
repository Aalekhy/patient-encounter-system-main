from alembic import op
import sqlalchemy as sa


revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "Alekhya_patients",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("email", sa.String(255), unique=True),
        sa.Column("phone", sa.String(20)),
        sa.Column("created_at", sa.DateTime(timezone=True)),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )

    op.create_table(
        "Alekhya_doctors",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("full_name", sa.String(150), nullable=False),
        sa.Column("specialization", sa.String(100), nullable=False),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("created_at", sa.DateTime(timezone=True)),
    )

    op.create_table(
        "Alekhya_appointments",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("patient_id", sa.Integer, sa.ForeignKey("Alekhya_patients.id")),
        sa.Column("doctor_id", sa.Integer, sa.ForeignKey("Alekhya_doctors.id")),
        sa.Column("start_time", sa.DateTime(timezone=True)),
        sa.Column("duration_minutes", sa.Integer),
        sa.Column("created_at", sa.DateTime(timezone=True)),
    )


def downgrade():
    op.drop_table("Alekhya_appointments")
    op.drop_table("Alekhya_doctors")
    op.drop_table("Alekhya_patients")
