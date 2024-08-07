FROM python:3.12.4-slim

# LABELS
LABEL maintainer="Iván Alejandro Marugán <hello@ialejandro.rocks>" \
      description="Bitbucket Bot for Google Chat"                  \
      version="1.0.0"

# APPLICATION
COPY app /app
COPY requirements.txt /requirements.txt

# INSTALL REQUIREMENTS
RUN pip install -r /requirements.txt

WORKDIR /app

# RUN APP
ENTRYPOINT ["gunicorn", "run:app"]
