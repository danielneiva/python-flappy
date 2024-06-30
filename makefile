install:
	pip install pygame
	pip install coverage

test:
	python -m unittest discover -s tests -p "*.py"

run:
	python FlappyBird.py