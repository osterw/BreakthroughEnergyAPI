.PHONY: run test

run:
	uvicorn src.main:app --reload

test:
	python -m unittest discover -s src/tests
