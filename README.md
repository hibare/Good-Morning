# Good-Morning

A :robot: bot which produces your daily Morning dose.

Bot is written in Python and packaged as a Docker image.

## What it does? :yum:

1. Extract News from Google News :newspaper:.
    Extract news based on topic and location.

2. Extract Whether information :sunflower:.
    Extract current weather and forecast for mentioned cities.

3. Send pings in Slack :boom:.

4. Runs a cron like job every day at 6.00 AM :clock6:

## How to run? :rocket:

1. Rename `.env.example` as `.env` and populate with all the values.

2. Run Docker

    ```shell
    docker run -d --env-file ./.env hibare/good-morning
    ```

                            *OR*

    using docker-compose

    ```shell
    docker-compose up -d
    ```