# Naomesh - Orchestrateur

```blank
                  /~    NAOMESH ONION OCHERSTRATOR
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
    Onion-->Postgresql
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
    Jobs <--> Rabbitmq
    Setup-Nodes-Task --> g5k-provider
    Step-Task --> g5k-provider
    Photogrammetry-prefect-flow --> Setup-Nodes-Task
    Photogrammetry-prefect-flow --> Step-Task
    subgraph EnosLib
    Ansible --> front

    g5k-provider --> Ansible
    g5k-provider --> Python-grid5000
    Python-grid5000
    end
    subgraph Tomodachi Services
    Jobs
    Amqp
    Schedule
    end
    end
    subgraph Grid 5000
    ecotype-X
    g5k-rest-api
    front --> ecotype-X
    end
    Rabbitmq
    Postgresql
```

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
