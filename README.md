# CC-Explorer
## Overview:
Docker container based WebApplication (created with CoockieCutter).
6 Docker Containers (ML in development):
- Vue Frontend Container
- PostgreSQL database container
- django backend container (communication between frontend-, database- and ML- containers)
- ML container using FastAPI and PyTorch for ML functions (In development)
- PgAdmin for database testing
- localDocs for documentations

## Requirements:
- npm installed (for frontend)


## Django installation for development
- sqlite3 database instead of postgres used
- create | activate django environment: conda create -n ENVNAME | conda activate ENVNAME
- install requirements: pip install -r local_nopg.txt
- if needed migrate, makemigrations and start server:
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver_plus 0.0.0.0:8000

## FastAPI for development
- source files in ml-docker
- create | activate ml-environment: conda create -n ENVNAME | conda activate ENVNAME
- run fastAPI server: python main.py