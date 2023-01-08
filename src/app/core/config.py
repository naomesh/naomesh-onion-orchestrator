import environ
import os

env = environ.Env(
    NAOMESH_ORCHESTRATOR_DEBUG=(bool, False),
    NAOMESH_ORCHESTRATOR_GRID5000_USERNAME=str,
    NAOMESH_ORCHESTRATOR_GRID5000_PASSWORD=str,
    NAOMESH_ORCHESTRATOR_GRID5000_VERIFY_SSL=str,
    NAOMESH_ORCHESTRATOR_GRID5000_TARGET_SITE=str
)

# Set the project base directory
BASE_DIR = os.path.abspath(os.path.join(__file__ ,"../../../.."))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))



