.PHONY: test deploy test-py2 test-py3 deploy-py2 deploy-py3 clean

PKG = HTMLMinifier

NOSE_PY2 = nosetests
NOSE_PY3 = nosetests-3.3
NOSE_OPTS = --with-coverage --cover-package $(PKG)

PY2 = python
PY3 = python3
DEPLOY_OPTS = sdist bdist_egg upload

all: test

test: test-py2 test-py3
deploy: deploy-py2 deploy-py3

test-py2:
	$(NOSE_PY2) $(NOSE_OPTS)

test-py3:
	$(NOSE_PY3) $(NOSE_OPTS)

deploy-py2:
	$(PY2) setup.py $(DEPLOY_OPTS)

deploy-py3:
	$(PY3) setup.py $(DEPLOY_OPTS)

clean:
	$(RM) -r $(PKG).egg-info
	$(RM) -r dist
	$(RM) -r build
