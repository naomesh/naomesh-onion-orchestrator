from app.core.config import env
from app.process.login import login
from app.process.tasks import reserve

import logging

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    g5k = login(
        username=env("NAOMESH_ORCHESTRATOR_GRID5000_USERNAME"),
        password=env("NAOMESH_ORCHESTRATOR_GRID5000_PASSWORD")
    )
    
    g5k.
    
    reservation = reserve(
        site=env("NAOMESH_ORCHESTRATOR_GRID5000_SITE"),
    )
    