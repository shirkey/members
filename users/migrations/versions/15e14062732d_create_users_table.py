"""create users table

Revision ID: 15e14062732d
Revises: None
Create Date: 2014-07-05 21:40:46.378774

"""
# revision identifiers, used by Alembic.
revision = '15e14062732d'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("guid", sa.String(37), nullable=False, unique=True),
        sa.Column("name", sa.String(32), nullable=False),
        sa.Column("email", sa.String(254), nullable=False),
        sa.Column("website", sa.String(255), default=""),
        sa.Column("email_updates", sa.Boolean(name="email_updates"),
                  default=False),
        sa.Column("date_added", sa.DateTime,
                  server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("latitude", sa.Float),
        sa.Column("longitude", sa.Float),
        )


def downgrade():
    op.drop_table("users")
