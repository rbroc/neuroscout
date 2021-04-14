"""empty message

Revision ID: 5231dab84bfd
Revises: e4e0613e3c58
Create Date: 2021-02-24 23:18:13.225422

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5231dab84bfd'
down_revision = 'e4e0613e3c58'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('predictor', sa.Column('min', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('predictor', 'min')
    # ### end Alembic commands ###
