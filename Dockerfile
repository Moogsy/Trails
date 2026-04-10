FROM python:3.14-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --uid 1000 appuser

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000