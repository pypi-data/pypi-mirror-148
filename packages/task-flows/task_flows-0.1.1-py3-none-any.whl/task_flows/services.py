import argparse
from typing import List, Optional

import sqlalchemy as sa
from sqlalchemy.engine import Engine

from . import containers, systemd
from .utils import scheduled_service_names


def create_services(engine: Engine, image_name: str, names: Optional[List[str]] = None):
    if isinstance(names, str):
        names = [names]
    elif names is None:
        names = scheduled_service_names(engine)
    containers.create_from_db(engine, image_name, names)
    systemd.install_from_db(engine, names)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--db-url",
        "-d",
        type=str,
        required=True,
        help="Address of postgresql database that holds the service environments and timers.",
    )
    parser.add_argument(
        "--image",
        "-i",
        type=str,
        required=True,
        help="Name of the Docker image that should be used to create containers.",
    )
    parser.add_argument(
        "--script-name",
        "-s",
        nargs="*",
        type=str,
        help="Name of installed script(s) that service should be created for.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    engine = sa.create_engine(args.db_url)
    create_services(engine, args.image, args.script_name)
    engine.dispose()


if __name__ == "__main__":
    main()
