from enoslib import g5k_api_utils
from app.core.config import env


# HACK: Tell Bapiste to create an api for this
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

# uri (str): The URL of the Grid5000 api.
#         username (str): The user login.
#         password (str): The user password.
#         verify_ssl (bool); Whether SSL certificates should be validated.
#         timeout (float): Timeout to use for requests to the Grid5000 API.
#         session (requests.Session): session to use
#         ssl_cert (str): path to the client certificate file for Grid5000 API
#         ssl_key (str): path to the client key file for Grid5000 API
