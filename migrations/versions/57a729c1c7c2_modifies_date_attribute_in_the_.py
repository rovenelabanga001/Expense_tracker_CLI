"""modifies date attribute in the Transaction model

Revision ID: 57a729c1c7c2
Revises: 991c2b6dda19
Create Date: 2024-12-18 22:54:09.708399

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '57a729c1c7c2'
down_revision: Union[str, None] = '991c2b6dda19'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###