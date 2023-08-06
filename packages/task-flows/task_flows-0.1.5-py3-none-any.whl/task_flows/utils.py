import os
from functools import cache
from typing import Dict, List

import sqlalchemy as sa
from sqlalchemy.engine import Engine

from .tables import environment, timers


@cache
def get_engine() -> Engine:
    """Create an Sqlalchemy engine using a Postgresql URL from environment variable."""
    var_name = "POSTGRES_URL"
    if not (url := os.getenv(var_name)):
        raise RuntimeError(
            f"Environment variable {var_name} is not set. Can not connect to database."
        )
    return sa.create_engine(url)


def get_env(name: str) -> Dict[str, str]:
    """Load environment variables for a container/script from the database table.

    Args:
        name (str): Name of the container/script that environment variables should be retrieved from.

    Returns:
        Dict[str, str]: Map variable name to value.
    """
    with get_engine().begin() as conn:
        environment_query = sa.select(
            environment.c.variable,
            environment.c.value
            # variables with 'default' name are applied everything.
        ).where(environment.c.name.in_(["default", name]))
        env = dict(conn.execute(environment_query).fetchall())
    return env


def get_scheduled_service_names() -> List[str]:
    """Get names of all containers/scripts the have entries in the timer table (i.e. the ones that are scheduled)

    Returns:
        List[str]: The container/script names.
    """
    with get_engine().begin() as conn:
        names_query = sa.select(timers.c.name.distinct())
        names = list(conn.execute(names_query).scalars())
    return names
