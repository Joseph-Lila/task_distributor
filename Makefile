isort:
	isort src/ tests/

test:
	pytest tests/

lint:
	pylint src/
