FROM python:3.8

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_VIRTUALENVS_CREATE=0

RUN adduser --uid 1000 --gecos --quiet --disabled-password app_user

RUN mkdir -p /usr/src/app \
    && chown app_user.app_user /usr/src/app
WORKDIR /usr/src/app

COPY --chown=app_user requirements.txt ./

ARG PIP_ARGS=
RUN set -eux \
    && apt update \
    && apt upgrade -y \
    && apt install -y curl\
    && pip3 install -r requirements.txt $PIP_ARGS \
    && apt autoremove -y \
    && rm -rf /root/.cache/pip /var/cache/apt

COPY --chown=app_user . .

USER app_user

CMD ["/usr/local/bin/gunicorn", "base_app.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]

