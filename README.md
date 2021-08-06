# Commenti Server

Back-end for [Commenti](https://github.com/sprkweb/commenti)

## How to install

### Option 1 (the easiest): Docker Compose

The easiest way to set this up is using docker-compose, which starts the back-end itself, nginx as a reverse proxy and a PostgreSQL database.

1. Create files with environment variables:

    ```sh
    cp .env.example .env
    cp .env.postgres.example .env.postgres
    ```

2. Customize the `.env` and `.env.postgres` files.
3. Then start docker-compose:

    ```sh
    docker-compose up
    ```

### Option 2: Without containers

This option is the best for development or in case if you want, for example, to use Commenti alongside with an existing database server and an HTTP server with your own configuration.

1. Configure environment variables:

    ```sh
    cp .env.example .env
    ```

2. Edit the `.env` file in order to connect to a database (PostgreSQL).
3. Install dependecies:

    ```sh
    python -m pip install pipenv
    pipenv install
    pipenv shell # this command enables virtual environment
    ```

4. Then you need to run your own HTTP server, for example, gunicorn + nginx (note: Commenti Server is powered by Django framework).

    For development, run server using this command:

    ```sh
    ./manage.py runserver
    ```
