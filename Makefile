.PHONY: run test restart

run:
	uvicorn src.main:app --reload

test:
	python -m unittest discover -s src/tests

restart:
	-pkill -f "uvicorn src.main:app" || true
	sleep 2
	make run
