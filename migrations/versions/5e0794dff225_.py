"""empty message

Revision ID: 5e0794dff225
Revises: 97bc91c1ea77
Create Date: 2017-10-15 13:58:35.841399

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e0794dff225'
down_revision = '97bc91c1ea77'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creator_user_id', sa.String(), nullable=True),
    sa.Column('creator_name', sa.String(), nullable=True),
    sa.Column('course_id', sa.String(), nullable=True),
    sa.Column('course_code', sa.String(), nullable=True),
    sa.Column('course_name', sa.String(), nullable=True),
    sa.Column('acad_year', sa.String(), nullable=True),
    sa.Column('semester', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('weekcode',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('week_code', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('courseStaff',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'course_id')
    )
    op.create_table('courseStudent',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'course_id')
    )
    op.create_table('group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('course_name', sa.String(), nullable=True),
    sa.Column('group_name', sa.String(), nullable=True),
    sa.Column('start_time', sa.Integer(), nullable=True),
    sa.Column('end_time', sa.Integer(), nullable=True),
    sa.Column('day_code', sa.Integer(), nullable=True),
    sa.Column('week_code', sa.Integer(), nullable=True),
    sa.Column('venue', sa.String(), nullable=True),
    sa.Column('group_type', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('groupStaff',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'group_id')
    )
    op.create_table('groupStudent',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'group_id')
    )
    op.create_table('session',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('week_name', sa.String(), nullable=True),
    sa.Column('start_date', sa.Integer(), nullable=True),
    sa.Column('end_date', sa.Integer(), nullable=True),
    sa.Column('attendance_start_time', sa.Integer(), nullable=True),
    sa.Column('code', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('attendance',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('remark', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['session_id'], ['session.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'session_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('attendance')
    op.drop_table('session')
    op.drop_table('groupStudent')
    op.drop_table('groupStaff')
    op.drop_table('group')
    op.drop_table('courseStudent')
    op.drop_table('courseStaff')
    op.drop_table('weekcode')
    op.drop_table('course')
    # ### end Alembic commands ###
