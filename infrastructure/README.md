# infrastructure

## Description
...

## Setup
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ansible-galaxy collection install community.postgresql
```

## Run playbook on target environment
```sh
ansible-playbook -i ./inventory.ini ./playbook.yml 
```
