from pathlib import Path

import environ
import os


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent.parent


env = environ.Env(
    NAOMESH_ORCHESTRATOR_DEBUG=(bool, False),
    NAOMESH_ORCHESTRATOR_GRID5000_USERNAME=str,
    NAOMESH_ORCHESTRATOR_GRID5000_PASSWORD=str,
    NAOMESH_ORCHESTRATOR_GRID5000_VERIFY_SSL=(bool, False),
    NAOMESH_ORCHESTRATOR_GRID5000_TIMEOUT=(float, None),
    NAOMESH_ORCHESTRATOR_GRID5000_SSLCERT=(str, None),
    NAOMESH_ORCHESTRATOR_GRID5000_SSLKEY=(str, None),
    NAOMESH_ORCHESTRATOR_GRID5000_SSLUSER=(str, "anonymous"),
    NAOMESH_ORCHESTRATOR_GRID5000_SITE=str,
    NAOMESH_ORCHESTRATOR_DOCKER_USERNAME=str,
    NAOMESH_ORCHESTRATOR_DOCKER_PASSWORD=str,
    NAOMESH_ORCHESTRATOR_DOCKER_OPENMVS_IMAGE_MVGMVSPIPELINE_COMMAND_NAME=(
        str,
        "mvgmvs",
    ),
    MQTT_BROKER_ADDRESS=str,
    MQTT_BROKER_PORT=str,
    MQTT_BROKER_LAUNCH_TASK_TOPIC=str,
    MQTT_BROKER_STATUS_TASK_TOPIC=str,
)

# Set the project base directory
BASE_DIR = os.path.abspath(get_project_root())

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
