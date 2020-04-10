VENV=$(CURDIR)/venv

.PHONY: install

all: $(VENV)/installed

$(VENV)/bin/pip:
	python3 -m venv venv

$(VENV)/installed: $(VENV)/bin/pip
	$(VENV)/bin/pip install -r requirements.txt
	touch $(VENV)/installed

install: $(VENV)/installed

hosts: install
	$(VENV)/bin/python oca_helper.py iplist > hosts

ansible: install
	$(VENV)/bin/ansible-playbook -i hosts site.yml

create: install
	$(VENV)/bin/python oca_helper.py create

destroy: install
	$(VENV)/bin/python oca_helper.py destroy

