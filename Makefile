isort:
	isort src/ tests/

test:
	pytest tests/ --asyncio-mode=strict

lint:
	pylint src/
