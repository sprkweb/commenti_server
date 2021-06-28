# Commenti Server

## How to run

Configure environment variables (you can create an .env file):

```code
DEBUG=True
SECRET_KEY='my-secure-secret-key'
ALLOWED_HOST=myhost
DATABASE_NAME=dbname
DATABASE_USER=dbuser
DATABASE_PASSWORD=dbpass
DATABASE_HOST=host
DATABASE_PORT=1234
```

Install dependecies:

```sh
python -m pip install pipenv
pipenv install
pipenv shell
```
