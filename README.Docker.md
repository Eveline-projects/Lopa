# Docker Setup Guide

This guide explains how to containerize and run the Lopa application using Docker.

## Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) or Docker Engine installed.

## Environment Configuration
Before running, ensure you have a `.env` file in the root directory (you can copy it from `.env.example`).
```bash
cp .env.example .env
```

### Building and running your application

When you're ready, start your application by running:
`docker compose up --build`.

Your application will be available at http://localhost:8000.

### Useful Docker Commands
* Run in background: docker compose up -d

*  Stop containers: docker compose down

*  View logs: docker compose logs -f

*  Execute commands (e.g., migrations): docker compose exec web python manage.py migrate

### Deploying your application to the cloud

First, build your image, e.g.: `docker build -t myapp .`.
If your cloud uses a different CPU architecture than your development
machine (e.g., you are on a Mac M1 and your cloud provider is amd64),
you'll want to build the image for that platform, e.g.:
`docker build --platform=linux/amd64 -t myapp .`.

Then, push it to your registry, e.g. `docker push myregistry.com/myapp`.

Consult Docker's [getting started](https://docs.docker.com/go/get-started-sharing/)
docs for more detail on building and pushing.

### References
* [Docker's Python guide](https://docs.docker.com/language/python/)