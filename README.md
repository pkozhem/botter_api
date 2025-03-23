# API for botter

---
### Technologies:

- FastAPI
- Redis
- PostgreSQL
- Kafka
- Docker
- uv

---
### Installation
1) Clone project
    ```commandline
    git clone https://github.com/pkozhem/botter_api.git
    ```
   
    ```commandline
    cd botter_api
    ```
2) Check if you have `uv` and `docker compose` on your local machine:
    ```commandline
    which uv
    ```

    ```commandline
    which docker-compose
    ```
    Otherwise, install [uv](https://docs.astral.sh/uv/getting-started/installation/) and [docker](https://docs.docker.com/engine/install/) with [docker-compose](https://docs.docker.com/compose/install/).
3) Up docker containers
    ```commandline
    docker-compose -f /path/to/project/botter_api/docker/docker-compose.yml -d build
    ```
4) Activate virtual env and install dependencies
    ```commandline
    uv venv
    source .venv/bin/activate
    ```

    ```commandline
    uv run
    ```
5) Run server
    ```commandline
    uvicorn app.main:app
    ```
