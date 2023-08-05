import argparse
from typing import List, Optional

from . import containers, systemd
from .utils import get_scheduled_service_names


def create_services(image_name: str, names: Optional[List[str]] = None):
    if isinstance(names, str):
        names = [names]
    elif names is None:
        names = get_scheduled_service_names()
    containers.create_containers(image_name, names)
    systemd.setup_services_and_timers(names)


def parse_args():
    parser = argparse.ArgumentParser()
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
    create_services(args.image, args.script_name)


if __name__ == "__main__":
    main()
