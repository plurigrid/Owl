"""Initial migration

Revision ID: cc799b49fec7
Revises: 
Create Date: 2024-02-21 14:42:43.699588

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'cc799b49fec7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def table_exists(name: str) -> bool:
    """Check if a table already exists."""
    inspector = Inspector.from_engine(op.get_bind())
    return name in inspector.get_table_names()

def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    if not table_exists('capture'):
        op.create_table('capture',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('capture_uuid', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('filepath', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.Column('device_type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('duration', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('id')
        )

    if not table_exists('location'):
        op.create_table('location',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('address', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('capture_uuid', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint('id')
        )
    if not table_exists('capturesegment'):
        op.create_table('capturesegment',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('filepath', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.Column('conversation_uuid', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('source_capture_id', sa.Integer(), nullable=False),
        sa.Column('duration', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['source_capture_id'], ['capture.id'], ),
        sa.PrimaryKeyConstraint('id')
        )
    if not table_exists('conversation'):
        op.create_table('conversation',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.Column('end_time', sa.DateTime(), nullable=True),
        sa.Column('conversation_uuid', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('device_type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('summary', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('short_summary', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('summarization_model', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('state', sa.Enum('CAPTURING', 'PROCESSING', 'COMPLETED', 'FAILED_PROCESSING', name='conversationstate'), nullable=False),
        sa.Column('capture_segment_file_id', sa.Integer(), nullable=True),
        sa.Column('primary_location_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['capture_segment_file_id'], ['capturesegment.id'], ),
        sa.ForeignKeyConstraint(['primary_location_id'], ['location.id'], ),
        sa.PrimaryKeyConstraint('id')
        )
    if not table_exists('transcription'):
        op.create_table('transcription',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('realtime', sa.Boolean(), nullable=False),
        sa.Column('model', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('transcription_time', sa.Float(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversation.id'], ),
        sa.PrimaryKeyConstraint('id')
        )
    if not table_exists('utterance'):
        op.create_table('utterance',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('start', sa.Float(), nullable=True),
        sa.Column('end', sa.Float(), nullable=True),
        sa.Column('spoken_at', sa.DateTime(), nullable=True),
        sa.Column('realtime', sa.Boolean(), nullable=False),
        sa.Column('text', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('speaker', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('transcription_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['transcription_id'], ['transcription.id'], ),
        sa.PrimaryKeyConstraint('id')
        )
    if not table_exists('word'):
        op.create_table('word',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('word', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('start', sa.Float(), nullable=True),
        sa.Column('end', sa.Float(), nullable=True),
        sa.Column('score', sa.Float(), nullable=True),
        sa.Column('speaker', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('utterance_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['utterance_id'], ['utterance.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('word')
    op.drop_table('utterance')
    op.drop_table('transcription')
    op.drop_table('conversation')
    op.drop_table('capturesegment')
    op.drop_table('location')
    op.drop_table('capture')
    # ### end Alembic commands ###