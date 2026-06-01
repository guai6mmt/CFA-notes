#!/usr/bin/env bash
set -euo pipefail

git pull --ff-only
docker compose config --quiet
docker compose build --pull notes
docker compose up -d --wait notes
docker compose ps notes
