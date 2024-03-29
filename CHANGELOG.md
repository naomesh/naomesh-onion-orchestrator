<a name="unreleased"></a>
## [Unreleased]


<a name="0.0.4"></a>
## [0.0.4] - 2023-02-24
### Docs
- changelog

### Feat
- change default host to 0.0.0.0

### Fix
- remove getting datetime
- use string date instead
- time aware object
- remove timestamp from db
- invalid date format
- invalid type in database
- remove prefect dep


<a name="0.0.3"></a>
## [0.0.3] - 2023-02-24
### Docs
- changelog

### Fix
- proper module orion launch
- require prefect orion
- remove prefect dep
- remove delay_transition


<a name="0.0.2"></a>
## [0.0.2] - 2023-02-23
### Chore
- add asyncio dep
- add dockerignore
- remove not used patch
- splash in readme
- add changelog

### Docs
- add todo
- add asyncapi schema and small typos fix
- add schematic

### Feat
- use quality from policy
- push final results in pipeline to database (not the schema)
- push results to database
- add new env variable to disable g5k_auto_jump
- start new threads in deamon mode
- add more logging on boostrap
- send jobs.finished when job is finished

### Fix
- invalid float timestamp
- delete result before push
- invalid jobstatus message format
- apply migrations at launch
- timestamp in ms


<a name="v0.0.1"></a>
## v0.0.1 - 2023-02-23
### Chore
- remove paho mqtt
- comment .env.example
- add comments
- delete useless mqtt subscriber
- add missing .env.example variables
- delete patch file
- rabbitmq and postgres env docker composer
- remove setup.py for patching prefect, we edit the code directly for working tree
- add launch configs for vscode
- initial coretaskpolicy implemetation
- add patch dep
- upgrade deps
- add setup.py files
- unify setup.cfg with pyprojet.toml
- insert spaces in vscode
- add simple dataset
- update requirements to last commit enoslib

### Feat
- delete orphonated flows at launch
- jobstatus and allocatednodes
- check if there is one node available before allocating
- working pipeline
- rename uploads
- implement current_allocated_nodes
- start tomodachi services at launch
- rework tasks to use sequential runner
- add new dotenv variables
- apply deployements at startup
- initial implementation of policies without pauses
- apply prefect config from dotenv file
- generation of seduce api client
- initial rabbitmq services implementation
- add prefect as a dep
- :card_file_box: Add Dockerfile for deployment
- add politic name argument
- launch orion at startup
- add versioneer
- initial pipeline implementation
- initial mqtt implem
- sync .env.example
- login implem
- :zap: Work on the enoslib integration
- initial implem

### Fix
- replace first instead for service path
- path to load services tomodachi
- run until complete instead of run
- remove useless allow_classic_ssh
- :memo: Upgrade enolib version for dockerhub login and prepare openmvs pipeline

### Refactor
- move task_input_hash to utils


[Unreleased]: https://github.com/naomesh/naomesh-onion-orchestrator/compare/0.0.4...HEAD
[0.0.4]: https://github.com/naomesh/naomesh-onion-orchestrator/compare/0.0.3...0.0.4
[0.0.3]: https://github.com/naomesh/naomesh-onion-orchestrator/compare/0.0.2...0.0.3
[0.0.2]: https://github.com/naomesh/naomesh-onion-orchestrator/compare/v0.0.1...0.0.2
