VENV   = .myenv
PYTHON = $(VENV)/bin/python

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install mazegenerator-2.1.0-py3-none-any.whl

run:
	$(PYTHON) pac-man.py config.json

clean:
	rm -rf src/__pycache__
	rm -rf src/.mypy_cache
	rm -rf src/parsing_config_file/__pycache__
	rm -rf .mypy_cache