ROOT_DIR=${PWD}

.DEFAULT_GOAL := help

# general
help:
	@echo "Type: make [rule]. Available options are:"
	@echo ""
	@echo "- help"
	@echo "- format"
	@echo "- setup"
	@echo ""
	@echo "- start"
	@echo "- test"
	@echo "- test-cov"
	@echo ""
	@echo "- docker-build"
	@echo "- docker-start"
	@echo "- docker-stop"
	@echo "- docker-restart"
	@echo "- docker-logs"
	@echo ""

format:
	black .

setup:
	python3 -m pip install -r requirements.txt --upgrade

start:
	uvicorn main:app --host 0.0.0.0 --port 8000  --log-level debug --reload

test:
	python3 -m pytest

test-cov:
	python3 -m pytest --cov=. --maxfail=1 tests/

docker-build:
	docker compose build

docker-start:
	docker compose up -d

docker-stop:
	docker compose down -v

docker-restart:
	docker compose restart

docker-logs:
	docker compose logs
