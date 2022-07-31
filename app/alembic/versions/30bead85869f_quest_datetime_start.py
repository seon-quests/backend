"""quest datetime start

Revision ID: 30bead85869f
Revises: 047206989442
Create Date: 2022-02-19 16:14:42.463465+02:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30bead85869f'
down_revision = '047206989442'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quest', sa.Column('start_datetime', sa.DateTime(), nullable=True))
    op.drop_column('quest', 'start_date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quest', sa.Column('start_date', sa.DATE(), autoincrement=False, nullable=True))
    op.drop_column('quest', 'start_datetime')
    # ### end Alembic commands ###
