FROM python:3.8.3-slim

# LABELS
LABEL maintainer="Iván Alejandro Marugán <hello@ialejandro.rocks>"                               \
      description="Cruise Control for Apache Kafka (https://github.com/linkedin/cruise-control)" \
      version="1.0.0"

# APPLICATION
COPY app /app
COPY requirements.txt /requirements.txt

# INSTALL REQUIREMENTS
RUN pip install -r /requirements.txt

WORKDIR /app

# RUN APP
ENTRYPOINT ["gunicorn", "run:app"]
