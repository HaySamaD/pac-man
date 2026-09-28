run:
	python3 pac-man.py config.json

clean:
	rm -rf src/__pycache__
	rm -rf src/.mypy_cache
	rm -rf src/parsing_config_file/__pycache__
	rm -rf .mypy_cache