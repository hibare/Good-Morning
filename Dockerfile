FROM python:3.9-alpine as build

RUN apk add libxml2-dev libxslt-dev python3-dev gcc build-base

RUN python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

FROM python:3.9-alpine as release

COPY --from=build /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY src /app

WORKDIR /app

ENTRYPOINT ["/opt/venv/bin/python", "runner.py"]
