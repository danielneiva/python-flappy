install:
	pip install pygame
	pip install coverage

test:
	coverage run -m unittest discover -s tests -p "*.py"
	coverage report
	coverage html

run:
	python FlappyBird.py