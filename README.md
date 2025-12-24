# Uptime Monitor

A simple uptime monitoring service that periodically checks a list of URLs,
stores the results in a PostgreSQL database, and provides a minimal web UI
to view recent check results.

The project is designed as a lightweight foundation for an uptime / health-check
system and is fully containerized using Docker Compose.

## Features

- Periodic HTTP checks for configured URLs
- PostgreSQL for persistent storage
- Simple web UI (Flask) to view results
- Docker Compose setup for easy local run

## Requirements

- Docker
- Docker Compose

## How to Run

1. Clone the repository:

```bash
git clone
cd uptime-monitor
```

2. Build and start the services:

```bash
docker compose up --build
```

3. Open the web UI in your browser:

```bash
http://localhost:5000
```

Adminer (database UI) is available at:

```bash
http://localhost:8080
```

## Configuration

URLs to monitor and other settings can be configured via environment variables
in docker-compose.yml:

- URLS – comma-separated list of URLs to check

- CHECK_INTERVAL – check interval in seconds
