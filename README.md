# Naomesh - ORCHESTRATOR

```blank
                  /~    NAOMESH ONION ORCHESTRATOR
                    \  \ /**     BUNDLED WITH
                    \ ////        ___ ___ ___ ___ _____________    ___ ___ ___  __   _  _
                    // //        | _ \ _ \ __| __| __/ __|_   _|  / _ \| _ \_ _/ _ \| \| |
                    // //        |  _/   / _|| _|| _| (__  | |   | (_) |   /| | (_) | .` |
                ///&//           |_| |_|_\___|_| |___\___| |_|    \___/|_|_\___\___/|_|\_|
                / & /\ \
                /  & .,,  \
            /& %  :       \
            /&  %   :  ;     `\
        /&' &..%   !..    `.\
        /&' : &''" !  ``. : `.\
        /#' % :  "" * .   : : `.\
        I# :& :  !"  *  `.  : ::  I
        I &% : : !%.` '. . : : :  I
        I && :%: .&.   . . : :  : I
        I %&&&%%: WW. .%. : :     I
        \&&&##%%%`W! & '  :   ,'/
        \####ITO%% W &..'  #,'/
            \W&&##%%&&&&### %./
                ++///~~\//_
                \\ \ \ \  \_
                /  /    \
```

## Onion schematics

```mermaid
flowchart TD
    GreenFlowPolicy --> SeduceRestApi
    SeduceRestApi --> SeduceGrafana
    subgraph Onion orchestrator
    subgraph Prefect
    Orion
    StateMachine
    GreenFlowPolicy
    SqlAlchemy
    end
    subgraph Scheduler
        Photogrammetry-prefect-flow
        Setup-Nodes-Task
        Step-Task

    end
    Photogrammetry-prefect-flow <-->|Before transition| GreenFlowPolicy
    StateMachine <--> GreenFlowPolicy
    Jobs ---> Photogrammetry-prefect-flow
    Setup-Nodes-Task --> g5k-provider
    Step-Task --> g5k-provider
    Photogrammetry-prefect-flow --> Setup-Nodes-Task
    Photogrammetry-prefect-flow --> Step-Task
    subgraph EnosLib

    G5k-provider --> Ansible
    G5k-provider --> Python-grid5000
    Python-grid5000
    end
    subgraph Tomodachi Services
    Jobs
    Amqp
    Schedule
    end
    end
    subgraph Grid 5000
    Ecotype-X
    G5k-rest-api
    Ansible --> Front
    Front --> Ecotype-X
    end
    Jobs <--> Rabbitmq
    Orion-->Postgresql
```

## Asyncapi

See
[docs/orion-ochestrator-async-api.yaml](docs/orion-ochestrator-async-api.yaml)

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
