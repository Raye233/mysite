"""empty message

Revision ID: d41769fafa3e
Revises: 11491c931a94
Create Date: 2025-03-13 22:34:41.756392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd41769fafa3e'
down_revision = '11491c931a94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('email_captcha', schema=None) as batch_op:
        batch_op.drop_index('email')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('email_captcha', schema=None) as batch_op:
        batch_op.create_index('email', ['email'], unique=True)

    # ### end Alembic commands ###
