"""empty message

Revision ID: a0c3cee6d2a8
Revises: 2b660507a1c9
Create Date: 2024-12-12 07:07:16.051276

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0c3cee6d2a8'
down_revision = '2b660507a1c9'
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
