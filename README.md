# Commenti Server

## How to run

Configure environment variables (you can create an .env file):

```code
DEBUG=True
SECRET_KEY='my-secure-secret-key'
ALLOWED_HOST=*
CORS_ALLOWED_ORIGIN_REGEX='^.*$'
DATABASE_NAME=postgres
DATABASE_USER=postgres
DATABASE_PASSWORD=123
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

Install dependecies:

```sh
python -m pip install pipenv
pipenv install
pipenv shell
```
