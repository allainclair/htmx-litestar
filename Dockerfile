# syntax=docker/dockerfile:1
# WIP
FROM python:3.12.1-alpine AS base
WORKDIR /app
# Manage curl and PDM
RUN apk update && \
    apk upgrade && \
    apk add curl && \
    curl -sSL https://pdm-project.org/install-pdm.py > install-pdm.py && \
    python3 install-pdm.py -p /usr && \
    rm install-pdm.py && \
    apk del curl
COPY pyproject.toml .


FROM base AS dev
RUN pdm update -dG "test,lint"
COPY src src
COPY tests tests


FROM base AS dev-debug
RUN pdm update -dG "test,lint,debug"
COPY src src
COPY tests tests


FROM base AS prod
RUN pdm install --prod
COPY src src


FROM dev AS tests
ENTRYPOINT ["pdm", "run", "lint-test"]


FROM prod AS prod-run
# Add the service to run
ENTRYPOINT ["pdm", "list", "--graph"]
