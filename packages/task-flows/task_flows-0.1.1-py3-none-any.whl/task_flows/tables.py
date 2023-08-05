from datetime import datetime

import sqlalchemy as sa

metadata = sa.MetaData(schema="services")

timers = sa.Table(
    "timers",
    metadata,
    sa.Column("name", sa.String, primary_key=True),
    sa.Column("keyword", sa.String, primary_key=True),
    sa.Column("value", sa.String),
)

environment = sa.Table(
    "environment",
    metadata,
    sa.Column("name", sa.String, primary_key=True),
    sa.Column("variable", sa.String, primary_key=True),
    sa.Column("value", sa.String),
)

task_table = sa.Table(
    "tasks",
    metadata,
    sa.Column("name", sa.String, primary_key=True),
    sa.Column(
        "started",
        sa.DateTime(timezone=False),
        default=datetime.utcnow,
        primary_key=True,
    ),
    sa.Column("finished", sa.DateTime(timezone=False)),
    sa.Column("retries", sa.Integer, default=0),
    sa.Column("status", sa.String),
    sa.Column("return_value", sa.String),
    sa.Column("errors", sa.String),
)
