"""changed search_id to search

Revision ID: 65eea4bc8373
Revises: 9aa1ce9d3159
Create Date: 2023-06-14 22:18:37.483141

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65eea4bc8373'
down_revision = '9aa1ce9d3159'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ARTICLES_REFERENCE', schema=None) as batch_op:
        batch_op.add_column(sa.Column('search', sa.Integer(), nullable=True))
        batch_op.drop_column('search_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ARTICLES_REFERENCE', schema=None) as batch_op:
        batch_op.add_column(sa.Column('search_id', sa.INTEGER(), nullable=True))
        batch_op.drop_column('search')

    # ### end Alembic commands ###