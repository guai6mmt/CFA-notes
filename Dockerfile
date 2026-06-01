FROM python:3.13-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python scripts/stage_docs.py
RUN mkdocs build --clean --strict

FROM caddy:2-alpine

COPY --from=builder /app/site /srv
COPY Caddyfile /etc/caddy/Caddyfile
