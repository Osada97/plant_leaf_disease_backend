"""First revision

Revision ID: 1af6c279ea8e
Revises: 
Create Date: 2022-02-22 01:30:08.474713

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1af6c279ea8e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('plants',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('plant_name', sa.String(length=155), nullable=False),
    sa.Column('science_name', sa.String(length=155), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_plants_id'), 'plants', ['id'], unique=False)
    op.create_table('plant_desease_medicines',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('medicene_type', sa.String(length=155), nullable=False),
    sa.Column('medicene_description', sa.Text(), nullable=False),
    sa.Column('plant_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['plant_id'], ['plants.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_plant_desease_medicines_id'), 'plant_desease_medicines', ['id'], unique=False)
    op.create_table('plant_deseases',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('desease_name', sa.String(length=155), nullable=False),
    sa.Column('desease_short_description', sa.String(length=155), nullable=False),
    sa.Column('symptoms', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('plant_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['plant_id'], ['plants.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_plant_deseases_id'), 'plant_deseases', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_plant_deseases_id'), table_name='plant_deseases')
    op.drop_table('plant_deseases')
    op.drop_index(op.f('ix_plant_desease_medicines_id'), table_name='plant_desease_medicines')
    op.drop_table('plant_desease_medicines')
    op.drop_index(op.f('ix_plants_id'), table_name='plants')
    op.drop_table('plants')
    # ### end Alembic commands ###
