import logging

# flake8: noqa
import app.enoslib.login
from app.scheduler.flows import reserve


logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":

    reservation = reserve()
