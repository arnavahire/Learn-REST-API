"""empty message

Revision ID: 8ef5605a6ffc
Revises: d802c86be7c3
Create Date: 2024-09-21 00:08:58.241433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ef5605a6ffc'
down_revision = 'd802c86be7c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(), nullable=False))
        batch_op.create_unique_constraint("email", ['email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint("email", type_='unique')
        batch_op.drop_column('email')

    # ### end Alembic commands ###