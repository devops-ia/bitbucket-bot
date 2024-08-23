ARG PYTHON_VERSION=3.12.5

FROM python:${PYTHON_VERSION}-alpine

LABEL maintainer="Iván Alejandro Marugán <hello@ialejandro.rocks>" \
      description="Bitbucket Bot for Google Chat"

COPY app /app
COPY Pipfile* /

RUN pip install pipenv && \
  pipenv sync --system

WORKDIR /app

ENTRYPOINT ["gunicorn", "run:app"]
