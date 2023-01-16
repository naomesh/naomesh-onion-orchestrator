import logging

# flake8: noqa
import app.process.login
from app.process.tasks import reserve

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":

    reservation = reserve()
