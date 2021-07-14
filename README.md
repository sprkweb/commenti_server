# Commenti Server

## How to run (using docker-compose)

Configure environment variables:

```sh
cp .env.example .env
cp .env.postgres.example .env.postgres
```

Edit the `.env` and `.env.postgres` files.

Then start docker-compose:

```sh
docker-compose up
```

## How to run (for development)

Configure environment variables:

```sh
cp .env.example .env
```

Edit the `.env` file in order to connect to a development database (PostgreSQL).

Install dependecies:

```sh
python -m pip install pipenv
pipenv install
pipenv shell
```

Run server:

```sh
./manage.py runserver
```
