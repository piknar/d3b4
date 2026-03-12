# d3b4 - Born of deby-lite, built to run in 512MB
# Agent Zero core: chat, utility, web3, venice.ai, MCP, A2A
# No browser, no torch, no TTS/STT - pure agent intelligence
FROM debian:trixie-slim

LABEL maintainer="piknar <piknar@gmail.com>"
LABEL description="d3b4 - Lean AI agent born of deby-lite, 512MB Docker"
LABEL version="0.1.0"
LABEL org.opencontainers.image.source="https://github.com/piknar/d3b4"
LABEL org.opencontainers.image.licenses="MIT"

ENV DEBIAN_FRONTEND=noninteractive

# Minimal system dependencies - no browser/X11 libs, no build tools at runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.13 \
    python3.13-venv \
    python3.13-dev \
    python3-pip \
    build-essential \
    gcc \
    g++ \
    pkg-config \
    git \
    curl \
    wget \
    ca-certificates \
    bash \
    procps \
    nano \
    unzip \
    zip \
    tar \
    rsync \
    jq \
    libxml2-dev \
    libxslt1-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /d3b4

# Create venv with Python 3.13
RUN python3.13 -m venv /d3b4/.venv && \
    /d3b4/.venv/bin/pip install --upgrade pip setuptools wheel

# Copy requirements first for layer caching
COPY requirements_d3b4.txt /tmp/requirements_d3b4.txt

# Install all dependencies
RUN /d3b4/.venv/bin/pip install --no-cache-dir -r /tmp/requirements_d3b4.txt

# Copy application code
COPY . /d3b4/

# Set environment variables
ENV A0_ROOT=/d3b4
ENV PYTHONPATH=/d3b4
ENV VIRTUAL_ENV=/d3b4/.venv
ENV PATH="/d3b4/.venv/bin:$PATH"
ENV IS_DOCKERIZED=true
ENV SHELL_INTERFACE=local
ENV A0_SET_SHELL_INTERFACE=local
ENV A0_SET_CODE_EXEC_SSH_ENABLED=false
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Startup script
COPY start_d3b4.sh /start_d3b4.sh
RUN chmod +x /start_d3b4.sh

EXPOSE 8080

ENTRYPOINT ["/start_d3b4.sh"]
