"""empty message

Revision ID: 12e0ea09d095
Revises: 074e1721c884
Create Date: 2025-04-14 20:37:09.552619

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '12e0ea09d095'
down_revision = '074e1721c884'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('avatar',
               existing_type=mysql.VARCHAR(length=10000),
               type_=sa.Text(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('avatar',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(length=10000),
               nullable=False)

    # ### end Alembic commands ###
