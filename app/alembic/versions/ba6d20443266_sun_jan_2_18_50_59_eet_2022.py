"""Sun Jan  2 18:50:59 EET 2022

Revision ID: ba6d20443266
Revises: e995a335ea2f
Create Date: 2022-01-02 18:50:59.595205+02:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba6d20443266'
down_revision = 'e995a335ea2f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('quest_stages_order_number_key', 'quest_stages', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('quest_stages_order_number_key', 'quest_stages', ['order_number'])
    # ### end Alembic commands ###
