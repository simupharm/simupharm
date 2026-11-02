"""Add billing/subscription fields and subscriptions table

Revision ID: 002_add_billing
Revises: 001_initial
Create Date: 2026-03-07

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002_add_billing'
down_revision: Union[str, None] = '001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add subscription fields to users table
    op.add_column('users', sa.Column('plan', sa.String(50), server_default='free'))
    op.add_column('users', sa.Column('stripe_customer_id', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('stripe_subscription_id', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('plan_expires_at', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('daily_simulation_count', sa.Integer(), server_default='0'))
    op.add_column('users', sa.Column('last_simulation_date', sa.String(10), nullable=True))

    # Create unique index on stripe_customer_id (nullable unique)
    op.create_index('ix_users_stripe_customer_id', 'users', ['stripe_customer_id'], unique=True)

    # Create subscriptions table
    op.create_table(
        'subscriptions',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('stripe_subscription_id', sa.String(255), nullable=True),
        sa.Column('stripe_checkout_session_id', sa.String(255), nullable=True),
        sa.Column('plan', sa.String(50), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='pending'),
        sa.Column('billing_period', sa.String(20), server_default='monthly'),
        sa.Column('amount', sa.Integer(), server_default='0'),
        sa.Column('currency', sa.String(3), server_default='INR'),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('canceled_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('subscriptions')
    op.drop_index('ix_users_stripe_customer_id', table_name='users')
    op.drop_column('users', 'last_simulation_date')
    op.drop_column('users', 'daily_simulation_count')
    op.drop_column('users', 'plan_expires_at')
    op.drop_column('users', 'stripe_subscription_id')
    op.drop_column('users', 'stripe_customer_id')
    op.drop_column('users', 'plan')
