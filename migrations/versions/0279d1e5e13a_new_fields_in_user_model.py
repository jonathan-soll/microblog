"""new fields in user model

Revision ID: 0279d1e5e13a
Revises: 302a6ab23179
Create Date: 2018-10-01 11:23:12.131928

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0279d1e5e13a'
down_revision = '302a6ab23179'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.String(length=140), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'about_me')
    # ### end Alembic commands ###
