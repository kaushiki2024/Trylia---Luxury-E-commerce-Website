"""add outfit3d table

Revision ID: 20250825_0002
Revises: 20250825_0001
Create Date: 2025-08-25 00:02:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '20250825_0002'
down_revision = '20250825_0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'outfit3d',
        sa.Column('model_id', sa.BigInteger(), primary_key=True),
        sa.Column('outfit_id', sa.BigInteger(), sa.ForeignKey('outfit.outfit_id', ondelete='CASCADE'), nullable=False),
        sa.Column('file_url', sa.String(length=1024), nullable=False),
        sa.Column('format', sa.String(length=16), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(op.f('ix_outfit3d_model_id'), 'outfit3d', ['model_id'], unique=False)
    op.create_index(op.f('ix_outfit3d_outfit_id'), 'outfit3d', ['outfit_id'], unique=False)
    op.create_unique_constraint('uq_outfit3d_outfit', 'outfit3d', ['outfit_id'])


def downgrade() -> None:
    op.drop_constraint('uq_outfit3d_outfit', 'outfit3d', type_='unique')
    op.drop_index(op.f('ix_outfit3d_outfit_id'), table_name='outfit3d')
    op.drop_index(op.f('ix_outfit3d_model_id'), table_name='outfit3d')
    op.drop_table('outfit3d')

