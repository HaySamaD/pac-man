install:
	pip install -r dependensices/requirements.txt
	pip install dependensices/mazegenerator-2.1.0-py3-none-any.whl

run:
	python3 pac-man.py config.json

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

debug:
	python3 -m pdb pac-man.py config.json

package:
	pyinstaller --onefile pac-man.py

clean:
	@rm -rf src/__pycache__
	@rm -rf src/d1_helpers/__pycache__
	@rm -rf src/d2_classes/__pycache__
	@rm -rf src/d3_parsing_config_file/__pycache__
	@rm -rf src/d4_parsing_highscores/__pycache__
	@rm -rf src/d5_display/__pycache__ src/d5_display/d1_helpers/__pycache__ src/d5_display/d2_game_pages/__pycache__
	@rm -rf src/d6_game_loop/__pycache__
	@rm -rf src/d5_display/d3_gameplay/__pycache__
