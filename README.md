# Commenti Server

Back-end for [Commenti](https://github.com/sprkweb/commenti)

## How to install

### Option 1 (the easiest): Docker Compose

The easiest way to set this up is using docker-compose, which starts the back-end itself, nginx as a reverse proxy and a PostgreSQL database.

1. [Download source code of this repo](https://github.com/sprkweb/commenti_server/releases)
2. Create files with environment variables:

    ```sh
    cp .env.example .env
    cp .env.postgres.example .env.postgres
    ```

3. Customize the `.env` and `.env.postgres` files.
4. Then start docker-compose:

    ```sh
    docker-compose up
    ```

### Option 2: Container

This option is the best in case if you want to use Commenti alongside with an existing database server and an HTTP server with your own configuration.

Download the Commenti container image from [the container registry](https://github.com/sprkweb/commenti_server/pkgs/container/commenti_server) and use it the way you would like.

See [docker-compose.yml](https://github.com/sprkweb/commenti_server/blob/master/docker-compose.yml) for a configuration example (volumes, environment, etc).

For example, in case you want to use HTTPS for your comments, you can follow the steps from Option 1, except that you need to configure [nginx](https://github.com/sprkweb/commenti_server/blob/master/nginx.conf) to use your SSL certificate.

### Option 3: Without containers

This option is the best for development.

1. [Download source code of this repo](https://github.com/sprkweb/commenti_server/releases)
2. Configure environment variables:

    ```sh
    cp .env.example .env
    ```

3. Edit the `.env` file in order to connect to a database (PostgreSQL).
4. Install dependecies:

    ```sh
    python -m pip install pipenv
    pipenv install
    pipenv shell # this command enables virtual environment
    ```

5. Create tables in the database:

    ```sh
    ./manage.py migrate
    ```

6. Create a superuser:

    ```sh
    ./manage.py createsuperuser
    ```

7. For production, you need to run your own HTTP server, for example, gunicorn + nginx (note: Commenti Server is powered by Django framework).

    For development, run server using this command:

    ```sh
    ./manage.py runserver
    ```
