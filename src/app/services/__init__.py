import os

from app.services.amqp import AmqpTransport  # noqa: F401
import app.services.jobs as jobs
import app.services.current_allocated_nodes as current_allocated_nodes

# A list of tomodachi services to start
# get relative paths from the current working directory, and strip the leading
# slash
SERVICES_TO_RUN = [
    jobs.__file__.replace(os.getcwd(), "", 1).strip("/"),
    current_allocated_nodes.__file__.replace(os.getcwd(), "", 1).strip("/"),
]
