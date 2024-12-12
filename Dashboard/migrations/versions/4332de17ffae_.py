"""empty message

Revision ID: 4332de17ffae
Revises: bb6b8760f084
Create Date: 2024-12-12 07:51:03.722748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4332de17ffae'
down_revision = 'bb6b8760f084'
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
