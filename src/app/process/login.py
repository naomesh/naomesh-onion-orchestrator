from app.core.config import env

import logging
import os

from grid5000 import Grid5000

def login():
    logging.basicConfig(level=logging.DEBUG)

    gk = Grid5000(
        username=env('NAOMESH_ORCHESTRATOR_GRID5000_USERNAME'),
        password=env('NAOMESH_ORCHESTRATOR_GRID5000_PASSWORD')
    )

    node_info = gk.sites["nancy"].clusters["grisou"].nodes["grisou-1"]

    print(
        "grisou-1 has {threads} threads and has {ram} bytes of RAM".format(
            threads=node_info.architecture["nb_threads"],
            ram=node_info.main_memory["ram_size"],
        )
    )
