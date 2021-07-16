FROM python:3.9-slim

### Environment configuration ###
#################################
EXPOSE 8000


# RUN apt-get update \
#     && apt-get install -y --no-install-recommends \
#         postgresql-client \
#     && rm -rf /var/lib/apt/lists/*


RUN groupadd -r worker --gid=999 \
    && useradd -m -r -g worker --uid=999 worker \
    && mkdir /static && chown worker:worker /static

USER worker
WORKDIR /home/worker

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=false

ENV STATIC_ROOT=/static

RUN pip install --user pipenv==2020.11.15
ENV PATH="/home/worker/.local/bin:${PATH}"

### Build ###
#############

COPY --chown=worker:worker Pipfile Pipfile.lock /home/worker/
RUN pipenv install

COPY --chown=worker:worker . /home/worker

RUN pipenv run ./manage.py collectstatic --noinput


ENTRYPOINT ["/home/worker/docker-entrypoint.sh"]
CMD ["pipenv", "run", \
    "gunicorn", \
    "--bind", "0.0.0.0:8000", \
    "--access-logfile", "-",  \
    "commenti_server.wsgi"]
