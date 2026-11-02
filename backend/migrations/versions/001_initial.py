"""Initial schema — Users, Experiments, QuizResults, Progress

Revision ID: 001_initial
Revises: None
Create Date: 2026-03-07

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('email', sa.String(255), unique=True, index=True, nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('institution', sa.String(255), server_default=''),
        sa.Column('role', sa.String(50), server_default='student'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        # Email verification fields
        sa.Column('is_verified', sa.Boolean(), server_default=sa.false()),
        sa.Column('verification_token', sa.String(255), nullable=True),
        sa.Column('verification_token_expires', sa.DateTime(), nullable=True),
        # Password reset fields
        sa.Column('password_reset_token', sa.String(255), nullable=True),
        sa.Column('password_reset_token_expires', sa.DateTime(), nullable=True),
    )

    # Experiments table
    op.create_table(
        'experiments',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('instrument', sa.String(50), nullable=False),
        sa.Column('compound_name', sa.String(255), server_default=''),
        sa.Column('parameters', sa.JSON(), server_default='{}'),
        sa.Column('results', sa.JSON(), server_default='{}'),
        sa.Column('notes', sa.Text(), server_default=''),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    # Quiz results table
    op.create_table(
        'quiz_results',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('instrument', sa.String(50), server_default='general'),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('total_questions', sa.Integer(), server_default='0'),
        sa.Column('time_taken_seconds', sa.Integer(), server_default='0'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    # Progress table
    op.create_table(
        'progress',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('instrument', sa.String(50), nullable=False),
        sa.Column('mastery_level', sa.Float(), server_default='0.0'),
        sa.Column('time_spent_minutes', sa.Integer(), server_default='0'),
        sa.Column('simulations_run', sa.Integer(), server_default='0'),
        sa.Column('last_accessed', sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('progress')
    op.drop_table('quiz_results')
    op.drop_table('experiments')
    op.drop_table('users')
