# Naomesh - Orchestrateur

## Setup

1. `pip install -r requirements.txt`
2. authentification
    1. `python3 src/auth.py`
    2. enter g5k password
3. ssh connexion
    1. generate ssh key with `ssh-keygen`
    2. `cat /home/user/.ssh/id_rsa.pub`
    3. go to https://api.grid5000.fr/stable/users/
    4. copy and paste public key in `ssh key`

## Dev setup

1. `pip install -r requirements-dev.txt`