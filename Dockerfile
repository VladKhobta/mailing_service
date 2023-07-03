FROM python:3.8-alpine3.12

#
WORKDIR .
COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
    libressl-dev
RUN apk add libpq
RUN pip install --upgrade pip setuptools
RUN apk add python3-dev
RUN apk add --no-cache postgresql-libs postgresql-dev
RUN pip install -r requirements.txt
RUN rm -rf /root/.cache/pip
