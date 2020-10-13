# Build

FROM python:3.9-alpine as build

RUN apk add libxml2-dev libxslt-dev gcc libc-dev

RUN python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

# Release

FROM python:3.9-alpine as release

LABEL Maintainer="Shubham Hibare"

LABEL Github="hibare"

COPY --from=build /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY src /app

WORKDIR /app

ENTRYPOINT ["/opt/venv/bin/python", "runner.py"]
