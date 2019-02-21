"""Create models

Revision ID: a0a279efb970
Revises: 
Create Date: 2019-01-05 15:44:17.613673

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0a279efb970'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('hashed_password', sa.String(length=80), nullable=True),
    sa.Column('account', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('account'),
    sa.UniqueConstraint('username')
    )
    op.create_table('cash_flow',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('type', sa.Integer(), nullable=False),
    sa.Column('bank_ref', sa.String(length=40), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('bank_ref')
    )
    op.create_table('decision',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('decision', sa.String(length=16), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=False),
    sa.Column('interest_daily', sa.Float(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('duration_days', sa.Integer(), nullable=True),
    sa.Column('repayment_frequency_days', sa.Integer(), nullable=True),
    sa.Column('fee_rate', sa.Float(), nullable=True),
    sa.Column('fee_amount', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('loan',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('start_datetime', sa.DateTime(), nullable=False),
    sa.Column('opening_balance', sa.Float(), nullable=False),
    sa.Column('duration_days', sa.Integer(), nullable=False),
    sa.Column('interest_daily', sa.Float(), nullable=False),
    sa.Column('repayment_frequency_days', sa.Integer(), nullable=False),
    sa.Column('repayment_amount', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('loan')
    op.drop_table('decision')
    op.drop_table('cash_flow')
    op.drop_table('user')
    # ### end Alembic commands ###