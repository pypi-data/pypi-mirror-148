import os
from functools import cache
from typing import Dict

import sqlalchemy as sa
from sqlalchemy.engine import Engine

from .tables import environment, timers


def load_env(engine: Engine, name: str) -> Dict[str, str]:
    # get any default environment variables.
    with engine.begin() as conn:
        environment_query = sa.select(
            environment.c.variable, environment.c.value
        ).where(environment.c.name.in_(["default", name]))
        env = dict(conn.execute(environment_query).fetchall())
    return env


def scheduled_service_names(engine: Engine):
    # get all script names.
    with engine.begin() as conn:
        names_query = sa.select(timers.c.name.distinct())
        names = list(conn.execute(names_query).scalars())
    return names


@cache
def get_engine() -> Engine:
    var_name = "POSTGRES_URL"
    if not (url := os.getenv(var_name)):
        raise RuntimeError(
            f"Environment variable {var_name} is not set. Can not connect to database."
        )
    return sa.create_engine(url)
