from pprint import pformat
from typing import Dict, List

import docker
from docker.models.containers import Container
from tqdm import tqdm

from .logging import logger
from .utils import get_env

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


def create_containers(image_name: str, scripts: List[str]):
    """Create a container for each executable script.

    Args:
        image_name (str): Name of the Docker image that should be used to create containers.
        scripts (List[str]): The scripts to create containers for (i.e. the command for the executable)
    """
    logger.info("Creating docker containers.")
    for script_name in tqdm(scripts):
        logger.info(f"Creating service for {script_name}")
        create_container(
            image_name=image_name,
            script_name=script_name,
            environment=get_env(script_name),
        )
