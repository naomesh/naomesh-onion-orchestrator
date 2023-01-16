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
    NAOMESH_ORCHESTRATOR_GRID5000_TARGET_SITE=str,
    NAOMESH_ORCHESTRATOR_DOCKER_USERNAME=(str, None),
    NAOMESH_ORCHESTRATOR_DOCKER_PASSWORD=(str, None),
)

# Set the project base directory
BASE_DIR = os.path.abspath(get_project_root())

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
