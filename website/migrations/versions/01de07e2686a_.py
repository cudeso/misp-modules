"""empty message

Revision ID: 01de07e2686a
Revises: 
Create Date: 2024-02-05 14:38:17.739081

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.exc import OperationalError


# revision identifiers, used by Alembic.
revision = '01de07e2686a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    try:
        with op.batch_alter_table('module', schema=None) as batch_op:
            batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=True, default=True))
    except OperationalError:
        print("Column 'is_active' already exist in 'module'")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('module', schema=None) as batch_op:
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###
