"""Create purchases table

Revision ID: 0003_create_purchases
Revises: 0002_create_flowers
Create Date: 2026-06-16 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = "0003_create_purchases"
down_revision = "0002_create_flowers"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "purchases",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("flower_id", sa.Integer(), sa.ForeignKey("flowers.id"), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.Enum("in_cart", "purchased", name="purchasestatus"), nullable=False, server_default="in_cart"),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("purchases")
