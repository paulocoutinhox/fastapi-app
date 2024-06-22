# Python FastAPI App

A FastAPI complete application with nice features and tests.

[![Test](https://github.com/paulocoutinhox/fastapi-app/actions/workflows/test.yml/badge.svg)](https://github.com/paulocoutinhox/fastapi-app/actions/workflows/test.yml)

[![codecov](https://codecov.io/gh/paulocoutinhox/fastapi-app/graph/badge.svg?token=SFNWCA8JQ4)](https://codecov.io/gh/paulocoutinhox/fastapi-app)

## What is included

- Senior organization support
- Database support
- Scheduler jobs support
- Test, mock and code coverage support
- Service layer support
- Pydantic support
- Rate limiter support
- CORS support
- Static files support
- Docker support (single and compose)
- Ready for production
- Support for Python version from 3.8 to 3.12

## Use Cases

APIs are essential for various types of applications, including:

- Mobile applications
- Progressive Web Applications (PWA)
- Single Page Applications (SPA)
- Microservices
- Internet of Things (IoT) applications
- Desktop applications that require online functionalities
- JAMstack websites and applications
- Low-Code and No-Code services like Bubble, FlutterFlow and others

## Start Locally

To start locally execute:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000  --log-level debug --reload
```

or

```bash
make start
```

## Docker Single

To build and start docker in single mode:

```bash
docker build -f Dockerfile.web -t fastapi-app .
docker run --rm -v ./:/app -p 8000:8000 fastapi-app
```

or

```bash
make docker-single-build
make docker-single-start
```

To use a different database url when run:

```bash
docker run --rm -v ./:/app -p 8000:8000 -e DATABASE_URL="sqlite:///./other.db" fastapi-app
```

## Docker Compose

To build and start docker compose with application and database:

```bash
docker compose build
docker compose up -d
```

or

```bash
make docker-compose-build
make docker-compose-start
```

To stop docker compose:

```bash
docker compose down
```

or

```bash
make docker-compose-stop
```

## Tests

To run tests execute:

```bash
python3 -m pytest
```

or

```bash
make test
```

To run tests execute with code coverage:

```bash
python3 -m pytest --cov=. --maxfail=1 tests/
```

or

```bash
make test-cov
```

## License

[MIT](http://opensource.org/licenses/MIT)

Copyright (c) 2024, Paulo Coutinho
