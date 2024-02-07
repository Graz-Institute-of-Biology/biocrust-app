How To - Project Documentation
======================================================================

Get Started
----------------------------------------------------------------------

Documentation can be written as rst files in `biocrust_app/docs`.

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

To build and serve docs, use the commands::

    docker compose -f local.yml up docs


1. uncomment django superuser settings in ./compose/local/django/start
2. Go to ./frontend, run::

    npm install

3. To build dist folder run::

    npm run build

4. go to the dockerfile with "cd .." and run::
    
    docker compose -f local.yml up -d --build

5. Got to ./frontend, run:: 
    
    npm run serve



Migrate::

    docker compose -f local.yml run --rm django python manage.py makemigrations
    docker compose -f local.yml run --rm django python manage.py migrate

Restart Django::
    
    docker compose -f local.yml run --rm django touch wsgi.py

    (docker compose -f local.yml run --rm django python manage.py migrate runserver)



Run Django locally for development

- sqlite3 database instead of postgres used

Create local environment for django requirements (set your own ENVNAME for your django environment)::

    conda create -n ENVNAME
    
    conda activate ENVNAME

Install requirements::

    pip install -r local_nopg.txt

If needed migrate, makemigrations and start server::
    
    python manage.py makemigrations

    python manage.py migrate

    python manage.py runserver_plus 0.0.0.0:8000


FastAPI for development

- source files in ml-docker

Create local environment for FastAPI requirements (set your own ENVNAME for your FastAPI environment)::

    conda create -n ENVNAME
    
    conda activate ENVNAME

run fastAPI server::

FastAPI for development

- source files in ml-docker

- run fastAPI server: python main.py

install segmentation-models-pytorch

- install albumentations with imgaug: pip install -U albumentations[imgaug]



Changes to files in `docs/_source` will be picked up and reloaded automatically.

`Sphinx <https://www.sphinx-doc.org/>`_ is the tool used to build documentation.

Docstrings to Documentation
----------------------------------------------------------------------

The sphinx extension `apidoc <https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html/>`_ is used to automatically document code using signatures and docstrings.

Numpy or Google style docstrings will be picked up from project files and available for documentation. See the `Napoleon <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/>`_ extension for details.

For an in-use example, see the `page source <_sources/users.rst.txt>`_ for :ref:`users`.

To compile all docstrings automatically into documentation source files, use the command:
    ::

        make apidocs


This can be done in the docker container:
    ::

        docker run --rm docs make apidocs
