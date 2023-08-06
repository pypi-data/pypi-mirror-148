import pytest
import sqlalchemy as sa
from task_flows.utils import create_missing_tables, get_engine


@pytest.fixture
def tables():
    # TODO temp db.
    create_missing_tables()
