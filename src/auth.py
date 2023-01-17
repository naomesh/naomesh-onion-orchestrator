from grid5000 import cli
from app.core.config import env

if __name__ == '__main__':
    cli.auth(env("NAOMESH_ORCHESTRATOR_GRID5000_USERNAME"))