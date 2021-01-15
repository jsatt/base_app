FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_VIRTUALENVS_CREATE=0
ENV USER=app_user

RUN adduser --uid 1000 --gecos --quiet --disabled-password $USER

RUN mkdir -p /usr/src/app \
    && chown $USER.$USER /usr/src/app
WORKDIR /usr/src/app

COPY --chown=$USER pyproject.toml poetry.lock ./

ARG POETRY_ARGS=
RUN set -eux \
    && apt update \
    && apt upgrade -y \
    && apt install -y curl\
    && pip3 install poetry \
    && poetry install --no-root --no-interaction $POETRY_ARGS \
    && apt autoremove -y \
    && rm -rf /root/.cache/pip /root/.cache/pypoetry /var/cache/apt

COPY --chown=$USER . .

USER $USER

CMD ["/usr/local/bin/gunicorn", "base_app.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]

