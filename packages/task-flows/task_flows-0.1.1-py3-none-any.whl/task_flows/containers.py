from pprint import pformat
from typing import Dict, List

import docker
from docker.models.containers import Container
from sqlalchemy.engine import Engine
from tqdm import tqdm

from .utils import load_env, logger

docker_client = docker.DockerClient(base_url="unix:///var/run/docker.sock")


def create_container(
    image_name: str,
    script_name: str,
    environment: Dict[str, str],
) -> Container:
    """Create a Docker container for running a script.

    Args:
        image_name (str): Name of the Docker image that should be used to create containers.
        script_name (str): Name of the executable that should be used in the container's command.
        environment (Dict[str, str]): Environmental variables that should be used in the container.

    Returns:
        Container: The created container.
    """
    # remove any existing container with this name.
    try:
        docker_client.containers.get(script_name).remove()
        logger.info(f"Removed existing container: {script_name}")
    except docker.errors.NotFound:
        pass

    kwargs = {
        "image": image_name,
        "name": script_name,
        "network_mode": "host",
        "detach": True,
        "environment": environment,
        "command": script_name,
    }
    logger.info(f"Creating Docker container for {script_name}:\n{pformat(kwargs)}")
    return docker_client.containers.create(**kwargs)


def create_from_db(engine: Engine, image_name: str, names: List[str]):
    logger.info("Creating docker containers.")
    for script_name in tqdm(names):
        logger.info(f"Creating service for {script_name}")
        create_container(
            image_name=image_name,
            script_name=script_name,
            environment=load_env(engine, script_name),
        )
