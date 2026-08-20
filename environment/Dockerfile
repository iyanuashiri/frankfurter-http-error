FROM ubuntu:24.04

WORKDIR /app

# RUN apt-get update && apt-get install -y \
#     curl \
#     git \
#     python3 \
#     && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:${PATH}"

COPY backend/ .

RUN uv python install
RUN uv sync