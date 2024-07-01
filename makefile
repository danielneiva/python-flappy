install:
	pip install pygame

unit-test:
	python -m unittest discover -s tests/unit -p "*.py"

integration-test:
	python -m unittest discover -s tests/integration -p "*.py"

run:
	python FlappyBird.py