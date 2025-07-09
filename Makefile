ROOT_DIR=${PWD}

.DEFAULT_GOAL := help

# general
help:
	@echo "Type: make [rule]. Available options are:"
	@echo ""
	@echo "- help"
	@echo "- format"
	@echo "- deps"
	@echo "- deps-update"
	@echo ""
	@echo "- start"
	@echo "- test"
	@echo "- test-cov"
	@echo ""
	@echo "- docker-single-build"
	@echo "- docker-single-start"
	@echo ""
	@echo "- docker-compose-build"
	@echo "- docker-compose-start"
	@echo "- docker-compose-stop"
	@echo "- docker-compose-restart"
	@echo "- docker-compose-logs"
	@echo ""

format:
	black .

deps:
	python3 -m pip install -r requirements.txt

deps-update:
	python3 -m pip install pip-check-updates
	pcu -u

start:
	uvicorn main:app --host 0.0.0.0 --port 8000  --log-level debug --reload

test:
	python3 -m pytest

test-cov:
	python3 -m pytest --cov=. --maxfail=1 tests/

docker-single-build:
	docker build -f Dockerfile.web -t fastapi-app .

docker-single-start:
	docker run --rm -v ./:/app -p 8000:8000 fastapi-app

docker-compose-build:
	docker compose build

docker-compose-start:
	docker compose up -d

docker-compose-stop:
	docker compose down -v

docker-compose-restart:
	docker compose restart

docker-compose-logs:
	docker compose logs
