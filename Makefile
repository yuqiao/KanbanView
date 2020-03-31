MAIN=things3_to_kanban.py
SRC_CORE=src
SRC_TEST=tests
DEST=$(SRC_CORE)/kanban.html
PYTHON=python3
PYDOC=pydoc3
PIP=pip3

help:
	@echo "Some available commands:"
	@echo " * run          - Run code."
	@echo " * open         - Open Kanban Board."
	@echo " * test         - Run unit tests and test coverage."
	@echo " * doc          - Document code (pydoc)."
	@echo " * clean        - Cleanup (e.g. pyc files)."
	@echo " * auto-style   - Automatially style code (autopep8)."
	@echo " * code-style   - Check code style (pycodestyle)."
	@echo " * code-lint    - Check code lints (pyflakes, pyline)."
	@echo " * code-count   - Count code lines (cloc)."
	@echo " * deps-install - Install dependencies (see requirements.txt)."
	@echo " * deps-update  - Update dependencies (via pur)."
	@echo " * feedback     - Create a GitHub issue."

run:
	@$(PYTHON) $(SRC_CORE)/$(MAIN)

test:
#	@type coverage >/dev/null 2>&1 || (echo "Run 'pip install coverage' first." >&2 ; exit 1)
#	@coverage run --source . -m $(SRC_TEST).test_getthings
#	@coverage report
	@echo "not implemented"

.PHONY: doc
doc:
#	@$(PYDOC) src.hello
	@echo "not implemented"

.PHONY: open
open:
	@open $(DEST)

.PHONY: clean
clean:
	@rm -f $(DEST)

auto-style:
	@type autopep8 >/dev/null 2>&1 || (echo "Run 'pip install autopep8' first." >&2 ; exit 1)
	@autopep8 -i -r $(SRC_CORE)

code-style:
	@type pycodestyle >/dev/null 2>&1 || (echo "Run 'pip install pycodestyle' first." >&2 ; exit 1)
	@pycodestyle --max-line-length=80 $(SRC_CORE)

code-lint:
	@type pyflakes >/dev/null 2>&1 || (echo "Run 'pip install pyflakes' first." >&2 ; exit 1)
	@type pylint >/dev/null 2>&1 || (echo "Run 'pip install pylint' first." >&2 ; exit 1)
	@type flake8 >/dev/null 2>&1 || (echo "Run 'pip install flake8' first." >&2 ; exit 1)
	@echo "PyFlakes:" ; pyflakes $(SRC_CORE)
	@echo "Flake8:" ; flake8 --max-complexity 10 $(SRC_CORE)
	@echo "PyLint:" ; pylint $(SRC_CORE)/*.py

code-count:
	@type cloc >/dev/null 2>&1 || (echo "Run 'brew install cloc' first." >&2 ; exit 1)
	@cloc $(SRC_CORE)

deps-update:
	@type pur >/dev/null 2>&1 || (echo "Run 'pip3 install pur' first." >&2 ; exit 1)
	@pur -r requirements.txt

deps-install:
	@type $(PIP) >/dev/null 2>&1 || (echo "Run 'curl https://bootstrap.pypa.io/get-pip.py|sudo python3' first." >&2 ; exit 1)
	@$(PIP) install -r requirements.txt

feedback:
	@open https://github.com/AlexanderWillner/KanbanView/issues