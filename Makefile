MAIN=things3_kanban
APP=things3_app
SERVER=things3_api
SERVER_PORT=8088
CLI=things3_cli
SRC_CORE=things3
SRC_TEST=tests
DEST=kanban-static.html
DEST_SRV=http://localhost:$(SERVER_PORT)/kanban.html
PYTHON=python3
PYDOC=pydoc3
PIP=pip3
PIPENV=pipenv

help:
	@echo "CLI, API and Web Service for Things3."
	@echo ""
	@echo "Configuration:"
	@echo " * Static Kanban : $(DEST)"
	@echo " * Dynamic Kanban: $(DEST_SRV)"
	@echo ""
	@echo "Avaliable environment variables:"
	@echo " * THINGSDB    - Path to database"
	@echo " * TAG_WAITING - Tag for tasks you are waiting for"
	@echo " * TAG_MIT     - Tag for most important tassk"
	@echo ""
	@echo "Available commands:"
	@echo " * run          - Run code in static mode."
	@echo " * open         - Open GUI in static mode."
	@echo " * run-api      - Run code in api mode."	
	@echo " * open-api     - Open GUI in api mode in the browser."
	@echo " * kill-api     - Kill code in api mode."
	@echo " * run-app      - Run code in app mode."
	@echo " * cli          - Run code in cli mode (use 'args' for arguments)."
	@echo " * app          - Create KanbanView App."
	@echo " * install      - Install the library and command line tools."
	@echo " * test         - Run unit tests and test coverage."
	@echo " * doc          - Document code (pydoc)."
	@echo " * clean        - Cleanup (e.g. pyc files)."
	@echo " * auto-style   - Automatially style code (autopep8)."
	@echo " * code-style   - Check code style (pycodestyle)."
	@echo " * code-lint    - Check code lints (pyflakes, pyline, flake8)."
	@echo " * css-lint     - Check CSS styke lints (csslint)."
	@echo " * js-lint      - Check JS code lints (jslint)."
	@echo " * html-lint    - Check HTML file lints (tidy)."
	@echo " * code-count   - Count code lines (cloc)."
	@echo " * deps-install - Install dependencies (see requirements.txt)."
	@echo " * feedback     - Create a GitHub issue."

run:
	@$(PYTHON) -m $(SRC_CORE).$(MAIN)
	@echo "File created: $(DEST)"

open:
	@open $(DEST)

run-api:
	@$(PYTHON) -m $(SRC_CORE).$(SERVER)

open-api:
	@open $(DEST_SRV)

kill-api:
	@lsof -nti:$(SERVER_PORT) | xargs kill

run-app:
	@$(PYTHON) -m $(SRC_CORE).$(APP)

cli:
	@$(PYTHON) -m $(SRC_CORE).$(CLI) $(args)

install:
	@python3 setup.py install
	@echo "You can now use 'things-cli', 'things-api' and 'things-kanban'"

test:
	@type coverage >/dev/null 2>&1 || (echo "Run 'pip install coverage' first." >&2 ; exit 1)
	@coverage erase
	@coverage run -a -m $(SRC_TEST).test_things3
	@coverage run -a -m $(SRC_TEST).test_things3_api
	@coverage run -a -m $(SRC_TEST).test_things3_cli
	@coverage run -a -m $(SRC_TEST).test_things3_kanban
	@coverage report

.PHONY: app
app: clean
	@$(PYTHON) setup.py py2app -A -s
	@hdiutil create dist/tmp.dmg -ov -volname "KanbanView" -fs HFS+ -srcfolder "dist"
	@hdiutil convert dist/tmp.dmg -format UDZO -o dist/KanbanView.dmg
	@rm dist/tmp.dmg
	@open dist

.PHONY: doc
doc:
	@$(PYDOC) $(SRC_CORE).things3

.PHONY: clean
clean:
	@rm -f $(DEST)
	@find . -name \*.pyc -delete
	@find . -name __pycache__ -delete
	@rm -rf build dist *.egg-info

auto-style:
	@type autopep8 >/dev/null 2>&1 || (echo "Run '$(PIP) install autopep8' first." >&2 ; exit 1)
	@autopep8 -i -r $(SRC_CORE) $(SRC_TEST)

lint: code-style code-lint css-lint js-lint html-lint

code-style:
	@type pycodestyle >/dev/null 2>&1 || (echo "Run '$(PIP) install pycodestyle' first." >&2 ; exit 1)
	@pycodestyle --max-line-length=80 $(SRC_CORE) $(SRC_TEST)

code-lint:
	@type pylint >/dev/null 2>&1 || (echo "Run '$(PIP) install pylint' first." >&2 ; exit 1)
	@type flake8 >/dev/null 2>&1 || (echo "Run '$(PIP) install flake8' first." >&2 ; exit 1)
	@type mypy >/dev/null 2>&1 || (echo "Run '$(PIP) install mypy' first." >&2 ; exit 1)
	@echo "Flake8:" ; flake8 --max-complexity 10 $(SRC_CORE) $(SRC_TEST)
	@echo "Mypy:" ; mypy $(SRC_CORE)
	@echo "Mypy:" ; mypy $(SRC_TEST)
	@echo "PyLint:" ; pylint $(SRC_CORE)/*.py $(SRC_TEST)/*.py

css-lint:
	@type csslint >/dev/null 2>&1 || (echo "Run 'npm install -g csslint' first." >&2 ; exit 1)
	@csslint --format=compact resources/*.css

js-lint:
	@type jslint >/dev/null 2>&1 || (echo "Run 'npm install -g jslint-node' first." >&2 ; exit 1)
	@jslint resources/*.js || true

html-lint:
	@type tidy >/dev/null 2>&1 || (echo "Run 'brew install tidy' first." >&2 ; exit 1)
	@tidy -qe resources/*.html

code-count:
	@type cloc >/dev/null 2>&1 || (echo "Run 'brew install cloc' first." >&2 ; exit 1)
	@cloc $(SRC_CORE)

deps-install:
	@type $(PIPENV) >/dev/null 2>&1 || (echo "Run 'brew install pipenv' first." >&2 ; exit 1)
	@$(PIPENV) install

feedback:
	@open https://github.com/AlexanderWillner/KanbanView/issues
