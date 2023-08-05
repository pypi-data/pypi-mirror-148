from functools import cache
from pathlib import Path
from subprocess import run
from textwrap import dedent
from typing import Dict, List, Tuple

import sqlalchemy as sa
from ready_logger import logger
from sqlalchemy.engine import Engine

from .tables import timers


@cache
def get_systemd_dir():
    d = Path.home() / ".config/systemd/user"
    d.mkdir(parents=True, exist_ok=True)
    return d


def install_systemd_service(container_name: str) -> Path:
    """Install a systemd service that can be used to run a container.

    Args:
        container_name (str): Name of container that the systemd service should run.

    Returns:
        Path: The path to the file.
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


def install_systemd_timer(
    container_name: str, timer_kwargs: List[Tuple[str, str]]
) -> str:
    systemd_dir = get_systemd_dir()
    timer_file = systemd_dir.joinpath(f"{container_name}.timer")
    timer_file.write_text(
        "\n".join(
            [
                "[Unit]",
                f"Description=Timer for script {container_name}",
                "[Timer]",
                *[f"{k}={v}" for k, v in timer_kwargs],
                "Persistent=true",
                "[Install]",
                "WantedBy=timers.target",
            ]
        )
    )
    logger.info(f"Installed Systemd timer for {container_name}: {timer_file}")
    return timer_file


def install(name_and_timer_kwargs: List[Tuple[str, Dict[str, str]]]):
    timer_names = []
    for name, timer_kwargs in name_and_timer_kwargs.items():
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


def install_from_db(engine: Engine, names: List[str]):
    if isinstance(names, str):
        names = [names]
    name_and_timer_kwargs = []
    with engine.begin() as conn:
        for name in names:
            timer_query = sa.select(timers.c.keyword, timers.c.value).where(
                timers.c.name == name
            )
            timer_kwargs = list(conn.execute(timer_query).fetchall())
            name_and_timer_kwargs.append((name, timer_kwargs))
    install(name_and_timer_kwargs)
