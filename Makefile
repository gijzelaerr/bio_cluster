VENV=$(CURDIR)/venv

.PHONY: install

all: ${VENV}/installed

${VENV}/bin/pip:
	python3 -m venv venv

${VENV}/installed: ${VENV}/bin/pip
	${VENV}/bin/pip install -r requirements.txt
	touch ${VENV}/installed

install: ${VENV}/installed

hosts: instyall
	${VENV}/bin/python oca_helper.py iplist > hosts

ansible: hosts
	${VENV}/bin/ansible-playbook -i hosts ansible.yml

create: install
	${VENV}/bin/python oca_helper.py create

destroy: install
	${VENV}/bin/python oca_helper.py destroy

