"""empty message

Revision ID: 97465eab4bc3
Revises: 
Create Date: 2017-10-05 11:16:36.469400

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97465eab4bc3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('metric', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('metric'),
    sa.UniqueConstraint('metric')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###