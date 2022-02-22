"""Drop nullable symotoms

Revision ID: 825381388566
Revises: bdd81ff9668a
Create Date: 2022-02-22 02:33:06.123985

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '825381388566'
down_revision = 'bdd81ff9668a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('plant_deseases', 'symptoms',
               existing_type=sa.TEXT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('plant_deseases', 'symptoms',
               existing_type=sa.TEXT(),
               nullable=False)
    # ### end Alembic commands ###