"""initial

Revision ID: 20250825_0001
Revises: 
Create Date: 2025-08-25 00:01:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20250825_0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('user_id', sa.BigInteger(), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=320), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(op.f('ix_user_user_id'), 'user', ['user_id'], unique=False)
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_unique_constraint('uq_user_email', 'user', ['email'])

    op.create_table(
        'outfit',
        sa.Column('outfit_id', sa.BigInteger(), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=False),
        sa.Column('image_url', sa.String(length=1024), nullable=False),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(op.f('ix_outfit_outfit_id'), 'outfit', ['outfit_id'], unique=False)

    op.create_table(
        'userphoto',
        sa.Column('photo_id', sa.BigInteger(), primary_key=True),
        sa.Column('user_id', sa.BigInteger(), sa.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False),
        sa.Column('image_url', sa.String(length=1024), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(op.f('ix_userphoto_photo_id'), 'userphoto', ['photo_id'], unique=False)
    op.create_index(op.f('ix_userphoto_user_id'), 'userphoto', ['user_id'], unique=False)

    op.create_table(
        'tryonsession',
        sa.Column('session_id', sa.BigInteger(), primary_key=True),
        sa.Column('user_id', sa.BigInteger(), sa.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False),
        sa.Column('photo_id', sa.BigInteger(), sa.ForeignKey('userphoto.photo_id', ondelete='SET NULL'), nullable=True),
        sa.Column('outfit_id', sa.BigInteger(), sa.ForeignKey('outfit.outfit_id', ondelete='SET NULL'), nullable=True),
        sa.Column('result_url', sa.String(length=1024), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(op.f('ix_tryonsession_session_id'), 'tryonsession', ['session_id'], unique=False)
    op.create_index(op.f('ix_tryonsession_user_id'), 'tryonsession', ['user_id'], unique=False)
    op.create_index(op.f('ix_tryonsession_photo_id'), 'tryonsession', ['photo_id'], unique=False)
    op.create_index(op.f('ix_tryonsession_outfit_id'), 'tryonsession', ['outfit_id'], unique=False)

    op.create_table(
        'recommendation',
        sa.Column('rec_id', sa.BigInteger(), primary_key=True),
        sa.Column('user_id', sa.BigInteger(), sa.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False),
        sa.Column('outfit_id', sa.BigInteger(), sa.ForeignKey('outfit.outfit_id', ondelete='CASCADE'), nullable=False),
        sa.Column('score', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(op.f('ix_recommendation_rec_id'), 'recommendation', ['rec_id'], unique=False)
    op.create_index(op.f('ix_recommendation_user_id'), 'recommendation', ['user_id'], unique=False)
    op.create_index(op.f('ix_recommendation_outfit_id'), 'recommendation', ['outfit_id'], unique=False)
    op.create_unique_constraint('uq_recommendation_user_outfit', 'recommendation', ['user_id', 'outfit_id'])


def downgrade() -> None:
    op.drop_constraint('uq_recommendation_user_outfit', 'recommendation', type_='unique')
    op.drop_index(op.f('ix_recommendation_outfit_id'), table_name='recommendation')
    op.drop_index(op.f('ix_recommendation_user_id'), table_name='recommendation')
    op.drop_index(op.f('ix_recommendation_rec_id'), table_name='recommendation')
    op.drop_table('recommendation')

    op.drop_index(op.f('ix_tryonsession_outfit_id'), table_name='tryonsession')
    op.drop_index(op.f('ix_tryonsession_photo_id'), table_name='tryonsession')
    op.drop_index(op.f('ix_tryonsession_user_id'), table_name='tryonsession')
    op.drop_index(op.f('ix_tryonsession_session_id'), table_name='tryonsession')
    op.drop_table('tryonsession')

    op.drop_index(op.f('ix_userphoto_user_id'), table_name='userphoto')
    op.drop_index(op.f('ix_userphoto_photo_id'), table_name='userphoto')
    op.drop_table('userphoto')

    op.drop_index(op.f('ix_outfit_outfit_id'), table_name='outfit')
    op.drop_table('outfit')

    op.drop_constraint('uq_user_email', 'user', type_='unique')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_index(op.f('ix_user_user_id'), table_name='user')
    op.drop_table('user')

