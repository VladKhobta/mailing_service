"""mailing constr

Revision ID: fca683288354
Revises: a9272aed2a91
Create Date: 2023-06-28 22:31:29.993833

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fca683288354'
down_revision = 'a9272aed2a91'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mailings', sa.Column('start_datetime', sa.DateTime(timezone=True), nullable=False))
    op.add_column('mailings', sa.Column('end_datetime', sa.DateTime(timezone=True), nullable=False))
    op.drop_column('mailings', 'mailing_datetime')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mailings', sa.Column('mailing_datetime', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False))
    op.drop_column('mailings', 'end_datetime')
    op.drop_column('mailings', 'start_datetime')
    # ### end Alembic commands ###
