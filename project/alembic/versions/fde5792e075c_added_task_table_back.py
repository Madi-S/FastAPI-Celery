"""Added task table back

Revision ID: fde5792e075c
Revises: f1da970ed535
Create Date: 2021-08-07 08:56:24.785004

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fde5792e075c'
down_revision = 'f1da970ed535'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('result', sa.String(), nullable=True),
    sa.Column('additional_data', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task')
    # ### end Alembic commands ###