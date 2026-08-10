FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl git

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:${PATH}"

COPY . .

RUN uv sync