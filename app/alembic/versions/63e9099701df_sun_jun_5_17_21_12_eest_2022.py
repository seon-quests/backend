"""Sun Jun  5 17:21:12 EEST 2022

Revision ID: 63e9099701df
Revises: a31ee84e625f
Create Date: 2022-06-05 17:21:13.284212+03:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63e9099701df'
down_revision = 'a31ee84e625f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quest_registered_teams', sa.Column('is_finished', sa.Boolean(), nullable=False))
    op.add_column('quest_registered_teams', sa.Column('is_started', sa.Boolean(), nullable=False))
    op.create_unique_constraint(None, 'quest_registered_teams', ['team_id', 'quest_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'quest_registered_teams', type_='unique')
    op.drop_column('quest_registered_teams', 'is_started')
    op.drop_column('quest_registered_teams', 'is_finished')
    # ### end Alembic commands ###
