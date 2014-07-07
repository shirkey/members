"""add social accounts

Revision ID: 49396d42bdab
Revises: 15e14062732d
Create Date: 2014-07-06 02:28:29.857087

"""

# revision identifiers, used by Alembic.
revision = '49396d42bdab'
down_revision = '15e14062732d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        "social_accounts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("guid", sa.String(37), sa.ForeignKey("users.guid")),
        sa.Column("twitter", sa.String(15)),
        )


def downgrade():
    op.drop_table("social_accounts")
