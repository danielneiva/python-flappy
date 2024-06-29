install:
	pip install pygame

test:
	python -m unittest discover -s tests -p "*.py"

run:
	python FlappyBird.py