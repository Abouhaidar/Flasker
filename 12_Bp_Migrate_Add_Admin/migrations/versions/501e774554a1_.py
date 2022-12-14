"""empty message

Revision ID: 501e774554a1
Revises: a46feba13bdc
Create Date: 2022-11-13 10:05:49.426443

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '501e774554a1'
down_revision = 'a46feba13bdc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('deleted_posts', 'posted_date')
    op.drop_column('deleted_posts', 'deleter')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('deleted_posts', sa.Column('deleter', sa.VARCHAR(length=100), nullable=False))
    op.add_column('deleted_posts', sa.Column('posted_date', sa.VARCHAR(), nullable=True))
    # ### end Alembic commands ###
