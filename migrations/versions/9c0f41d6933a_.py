"""empty message

Revision ID: 9c0f41d6933a
Revises: None
Create Date: 2016-07-29 19:29:13.059892

"""

# revision identifiers, used by Alembic.
revision = '9c0f41d6933a'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('devicePorts', sa.Column('gateway', sa.String(length=32), nullable=True))
    op.add_column('devicePorts', sa.Column('mask', sa.String(length=32), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('devicePorts', 'mask')
    op.drop_column('devicePorts', 'gateway')
    ### end Alembic commands ###
