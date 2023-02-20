import os

from app.services.amqp import AmqpTransport  # noqa: F401
import app.services.jobs as jobs
import app.services.currentallocatednodes as currentallocatednodes

# A list of tomodachi services to start
SERVICES_TO_RUN = [
    jobs.__file__.replace(os.getcwd(), ""),
    currentallocatednodes.__file__.replace(os.getcwd(), ""),
]
