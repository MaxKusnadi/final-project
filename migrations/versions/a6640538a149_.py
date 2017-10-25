"""empty message

Revision ID: a6640538a149
Revises: 03a65451f783
Create Date: 2017-10-25 14:26:40.863486

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6640538a149'
down_revision = '03a65451f783'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('courseStaff', sa.Column('is_attached_to_group', sa.Boolean(), nullable=True))
    op.add_column('session', sa.Column('attendance_closed_time', sa.Integer(), nullable=True))
    op.drop_column('session', 'attendance_start_time')
    op.drop_column('session', 'is_open')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('session', sa.Column('is_open', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('session', sa.Column('attendance_start_time', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('session', 'attendance_closed_time')
    op.drop_column('courseStaff', 'is_attached_to_group')
    # ### end Alembic commands ###