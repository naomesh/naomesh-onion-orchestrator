<a name="unreleased"></a>
## [Unreleased]


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


[Unreleased]: https://github.com/naomesh/naomesh-onion-orchestrator/compare/v0.0.1...HEAD
