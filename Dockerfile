ARG PYTHON_VERSION=3.12.5

FROM python:${PYTHON_VERSION}

LABEL maintainer="Iván Alejandro Marugán <hello@ialejandro.rocks>" \
      description="Bitbucket Bot for Google Chat"

COPY app /app
COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

WORKDIR /app

ENTRYPOINT ["gunicorn", "run:app"]
