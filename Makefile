VENV=$(CURDIR)/venv

all: ${VENV}/installed

${VENV}/bin/pip:
	python3 -m venv venv

${VENV}/installed: ${VENV}/bin/pip
	${VENV}/bin/pip install -r requirements.txt
	touch ${VENV}/installed
