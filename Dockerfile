FROM python:3.10.6-slim-buster
LABEL maintainer="chumak7377@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR app/

RUN apt-get update \
  # Additional dependencies
  && apt-get install -y procps \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.8000"]

RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user

USER django-user
