VENV   = .myenv
PYTHON = $(VENV)/bin/python

.PHONY: all install run clean fclean

all: install

$(VENV):
	python3 -m venv $(VENV)

install: $(VENV)
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install mazegenerator-2.1.0-py3-none-any.whl

run:
	$(PYTHON) pac-man.py

clean:
	rm -rf src/__pycache__
	rm -rf src/.mypy_cache
	rm -rf src/parsing_config_file/__pycache__
	rm -rf .mypy_cache
	rm -rf __pycache__
	rm -rf src/d0_helpers/__pycache__
	rm -rf src/d1_classes/__pycache__

fclean: clean
	rm -rf $(VENV)