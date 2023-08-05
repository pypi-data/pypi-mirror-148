from functools import cache
from pathlib import Path
from subprocess import run
from textwrap import dedent
from typing import List, Tuple

import sqlalchemy as sa
from tqdm import tqdm

from .logging import logger
from .tables import timers
from .utils import get_engine


@cache
def get_systemd_dir() -> Path:
    d = Path.home() / ".config/systemd/user"
    d.mkdir(parents=True, exist_ok=True)
    return d


def install_systemd_service(container_name: str) -> Path:
    """Install a systemd service that can be used to run a container.

    Args:
        container_name (str): Name of container that the systemd service should run.

    Returns:
        Path: The path to the installed file.
    """
    systemd_dir = get_systemd_dir()
    service_file = systemd_dir.joinpath(f"{container_name}.service")
    service_file.write_text(
        dedent(
            f"""
            [Unit]
            Description=script -- {container_name}
            After=network.target
            
            [Service]
            Type=simple
            ExecStart=docker start {container_name}
            
            # not needed if only using timer.
            [Install]
            WantedBy=multi-user.target
            """
        )
    )
    logger.info(f"Installed Systemd service for {container_name}: {service_file}")
    return service_file


def install_systemd_timer(name: str, timer_kwargs: List[Tuple[str, str]]) -> Path:
    """Install a systemd timer for running a container at specified time(s)

    Args:
        name (str): The name of the script/container/systemd service.
        timer_kwargs (List[Tuple[str, str]]): Keyword arguments for the [Timer] secion (e.g. OnCalendar)

    Returns:
        Path: Path to the installed file.
    """
    systemd_dir = get_systemd_dir()
    timer_file = systemd_dir.joinpath(f"{name}.timer")
    timer_file.write_text(
        "\n".join(
            [
                "[Unit]",
                f"Description=Timer for script {name}",
                "[Timer]",
                *[f"{k}={v}" for k, v in timer_kwargs],
                "Persistent=true",
                "[Install]",
                "WantedBy=timers.target",
            ]
        )
    )
    logger.info(f"Installed Systemd timer for {name}: {timer_file}")
    return timer_file


def setup_services_and_timers(names: List[str]):
    """Install and enable services and timers, using timer keyword arguments from the database table.

    Args:
        name_and_timer_kwargs (List[str]): Names of container/script.
    """
    if isinstance(names, str):
        names = [names]

    timer_names = []
    with get_engine().begin() as conn:
        for name in tqdm(names):
            timer_query = sa.select(timers.c.keyword, timers.c.value).where(
                timers.c.name == name
            )
            # timer_kwargs has to be a list of tuples (not dict), b/c there can be duplicate keys.
            timer_kwargs = list(conn.execute(timer_query).fetchall())
            install_systemd_service(name)
            timer_file = install_systemd_timer(name, timer_kwargs)
            timer_names.append(timer_file.name)
    logger.info("Reloading systemd services.")
    # make sure updated services are recognized.
    run(["systemctl", "--user", "daemon-reload"])
    # enable all timers.
    for timer_name in timer_names:
        logger.info(f"Enabling timer: {timer_name}")
        run(["systemctl", "--user", "enable", "--now", timer_name])
