# Introduction
Tooling for setting up an Arvados Bio cluster at SURFsara

# links

## the COVID-19 hackathon
 * https://github.com/virtual-biohackathons/covid-19-bh20

## The SURFsara HPC cloud
 * https://ui.hpccloud.surfsara.nl/
 * https://doc.hpccloud.surfsara.nl/

## arvados
 * https://arvados.org/
 * https://doc.arvados.org/v2.0/install/install-manual-prerequisites.html


# Get started

Read the top of init.py and follow the instructions

```
python3 -m venv env3
. env3/bin/activate
pip install -U pip
pip install -U setuptools wheel
pip install -rrequirements.txt
python init.py
```

Then transform the output into ".ini" format and update the "hosts" file

# The configuration

## main server
1 node
16+ GiB RAM
4+ cores
fast disk for database

roles:
 - Postgres database
 - Arvados API server
 - Arvados controller
 - Git
 - Websockets
 - Container dispatcher	1	

## SSO
1 node
2 GB ram

roles:
 - Single Sign-On (SSO)
 
## Workbench
1 node
8 GB ram
2+ cores

roles:
 - Workbench
 - Keep_proxy
 - Keep_web
 - Keep_balance
 
## keepstore servers
2+ nodes
4 GiB RAM

roles:
 - keepstore

## compute worker nodes
0+ nodes
Depends on workload; scaled dynamically in the cloud

roles:
 -  worker

## user shell nodes
0+
Depends on workload

roles:
  - shell
