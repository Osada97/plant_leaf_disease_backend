"""add unique constraints for username and email

Revision ID: 396aa59a4970
Revises: 4e23305fa470
Create Date: 2022-03-09 01:38:05.888539

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '396aa59a4970'
down_revision = '4e23305fa470'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'Users', ['email'])
    op.create_unique_constraint(None, 'Users', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Users', type_='unique')
    op.drop_constraint(None, 'Users', type_='unique')
    # ### end Alembic commands ###
