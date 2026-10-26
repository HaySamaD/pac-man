run:
	python3 pac-man.py config.json

clean:
	@rm -rf src/__pycache__
	@rm -rf src/.mypy_cache
	@rm -rf src/parsing_config_file/__pycache__
	@rm -rf .mypy_cache
	@rm -rf src/d0_helpers/.mypy_cache
	@rm -rf src/d1_classes/.mypy_cache
	@rm -rf src/d2_parsing_config_file/.mypy_cache
	@rm -rf src/d3_parsing_highscores/.mypy_cache
	@rm -rf src/d4_game_manager/.mypy_cache
	@rm -rf src/d5_display/.mypy_cache
	@rm -rf src/d4_display/.mypy_cache
	@rm -rf src/d1_classes/__pycache__
	@rm -rf src/d2_parsing_config_file/__pycache__
	@rm -rf src/d3_parsing_highscores/__pycache__
	@rm -rf src/d0_helpers/__pycache__
	@rm -rf src/d4_display/__pycache__
	@rm -rf /home/ybajdou/1-my_projects/pac-man/src/d5_game_loop/__pycache__