# Month 1 Capstone: Q&A API

A production-ready Q&A API built with FastAPI, async PostgreSQL, pgvector, Redis, and OpenAI.

## Architecture

* **Framework**: FastAPI with `asyncio`
* **Data Plane**: PostgreSQL with `pgvector`
* **State & Cache**: Redis
* **Observability**: OpenTelemetry tracing and structured JSON logging
* **Identity**: JWT with Argon2 password hashes

## Local Development

Copy the `.env.example` to `.env` and fill in the missing keys (e.g., your OpenAI API Key).

```bash
cp .env.example .env
```

Start the dependencies using Docker Compose:

```bash
docker-compose up -d
```

Install the local environment:

```bash
make install
```

Run the server locally:

```bash
make dev
```
