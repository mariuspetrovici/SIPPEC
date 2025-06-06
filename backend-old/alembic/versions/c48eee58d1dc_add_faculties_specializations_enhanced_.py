"""Add faculties, specializations, enhanced users and requests tables

Revision ID: c48eee58d1dc
Revises: 
Create Date: 2025-03-04 19:15:22.944611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c48eee58d1dc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('faculties',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_faculties_id'), 'faculties', ['id'], unique=False)
    op.create_index(op.f('ix_faculties_name'), 'faculties', ['name'], unique=True)
    op.create_table('rooms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_rooms_id'), 'rooms', ['id'], unique=False)
    op.create_table('specializations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('faculty_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['faculty_id'], ['faculties.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_specializations_id'), 'specializations', ['id'], unique=False)
    op.create_index(op.f('ix_specializations_name'), 'specializations', ['name'], unique=True)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('role', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('specialization_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['specialization_id'], ['specializations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('exams',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject', sa.String(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('room_id', sa.Integer(), nullable=True),
    sa.Column('proposed_by', sa.Integer(), nullable=True),
    sa.Column('confirmed_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['confirmed_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['proposed_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exams_id'), 'exams', ['id'], unique=False)
    op.create_table('requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('requester_id', sa.Integer(), nullable=True),
    sa.Column('handler_id', sa.Integer(), nullable=True),
    sa.Column('exam_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['exam_id'], ['exams.id'], ),
    sa.ForeignKeyConstraint(['handler_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['requester_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_requests_id'), 'requests', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_requests_id'), table_name='requests')
    op.drop_table('requests')
    op.drop_index(op.f('ix_exams_id'), table_name='exams')
    op.drop_table('exams')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_specializations_name'), table_name='specializations')
    op.drop_index(op.f('ix_specializations_id'), table_name='specializations')
    op.drop_table('specializations')
    op.drop_index(op.f('ix_rooms_id'), table_name='rooms')
    op.drop_table('rooms')
    op.drop_index(op.f('ix_faculties_name'), table_name='faculties')
    op.drop_index(op.f('ix_faculties_id'), table_name='faculties')
    op.drop_table('faculties')
    # ### end Alembic commands ###
