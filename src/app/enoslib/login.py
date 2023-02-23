from enoslib import g5k_api_utils
from app.core.config import env


# HACK: Tell Bapiste to create an api for this
# It monkey patch python-g5k
with g5k_api_utils._api_lock:
    if not g5k_api_utils._api_client:
        g5k_api_utils._api_client = g5k_api_utils.Client(
            username=env("NAOMESH_ORCHESTRATOR_GRID5000_USERNAME"),
            password=env("NAOMESH_ORCHESTRATOR_GRID5000_PASSWORD"),
            verify_ssl=env("NAOMESH_ORCHESTRATOR_GRID5000_VERIFY_SSL"),
            timeout=env("NAOMESH_ORCHESTRATOR_GRID5000_TIMEOUT"),
            session=None,
            sslcert=env("NAOMESH_ORCHESTRATOR_GRID5000_SSLCERT"),
            sslkey=env("NAOMESH_ORCHESTRATOR_GRID5000_SSLKEY"),
            ssluser=env("NAOMESH_ORCHESTRATOR_GRID5000_SSLUSER"),
        )
