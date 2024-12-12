"""empty message

Revision ID: 330ce852f294
Revises: 091eb4233f9a
Create Date: 2024-12-12 07:20:56.733158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '330ce852f294'
down_revision = '091eb4233f9a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sensor_readings', schema=None) as batch_op:
        batch_op.drop_index('ix_sensor_readings_timestamp')
        batch_op.create_index(batch_op.f('ix_sensor_readings_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sensor_readings', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_sensor_readings_timestamp'))
        batch_op.create_index('ix_sensor_readings_timestamp', ['timestamp'], unique=False)

    # ### end Alembic commands ###
