"""Configure the columns

Revision ID: 4ce3c903eed1
Revises: 
Create Date: 2022-06-16 21:03:55.318680

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ce3c903eed1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'name',
               existing_type=sa.VARCHAR(length=30))
    op.alter_column('users', 'location',
               existing_type=sa.VARCHAR(length=60))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'location',
               existing_type=sa.VARCHAR(length=60),
               nullable=False)
    op.alter_column('users', 'name',
               existing_type=sa.VARCHAR(length=30),
               nullable=False)
    # ### end Alembic commands ###
