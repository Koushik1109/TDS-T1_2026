---
title: ga2-b0b396
sdk: docker
app_port: 7073
description: deployment-ready-ga2-b0b396
suggested_hardware: cpu-basic
---

# GA2 Space

This Space runs a minimal FastAPI app on port 7073 using the Docker SDK.

- Docker: uses python:3.11-slim and switches to a non-root user with UID 1000.
- Port: `7073` (configured via `APP_PORT`).

## Deploy to Hugging Face Spaces

```bash
pip install -r requirements-deploy.txt
export HF_TOKEN=your_huggingface_token   # Windows: set HF_TOKEN=your_token
python deploy_space.py
```

Paste the printed public Space URL into the grader after the build succeeds.

## Run locally

```bash
docker build -t ga2-app .
docker run -p 7073:7073 ga2-app
```
