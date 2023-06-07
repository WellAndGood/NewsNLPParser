"""Add title column to SEARCHES_REFERENCE table

Revision ID: 6e307a1b5e62
Revises: 
Create Date: 2023-06-05 18:52:19.410985

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e307a1b5e62'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('SEARCHES_REFERENCE', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(length=250), nullable=True))
        batch_op.alter_column('url',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.String(length=300),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('SEARCHES_REFERENCE', schema=None) as batch_op:
        batch_op.alter_column('url',
               existing_type=sa.String(length=300),
               type_=sa.VARCHAR(length=200),
               existing_nullable=True)
        batch_op.drop_column('title')

    # ### end Alembic commands ###