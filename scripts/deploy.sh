#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

fail() {
  printf 'Error: %s\n' "$*" >&2
  exit 1
}

command -v git >/dev/null 2>&1 || fail "git is required."
command -v docker >/dev/null 2>&1 || fail "docker is required. Install Docker Engine and the Docker Compose plugin."
docker compose version >/dev/null 2>&1 || fail "the Docker Compose plugin is required."
docker info >/dev/null 2>&1 || fail "the Docker service is not running or the current user cannot access it."
docker compose up --help | grep -q -- '--wait' || fail "docker compose up --wait is required. Upgrade the Docker Compose plugin."

printf 'Updating source code...\n'
git pull --ff-only

printf 'Validating Compose configuration...\n'
docker compose config --quiet

printf 'Building the site image...\n'
docker compose build --pull notes

printf 'Starting the site and waiting for its health check...\n'
if ! docker compose up -d --wait notes; then
  printf '\nDeployment failed. Current container status:\n' >&2
  docker compose ps notes >&2 || true
  printf '\nRecent container logs:\n' >&2
  docker compose logs --tail=200 notes >&2 || true
  exit 1
fi
docker compose ps notes

published_address="$(docker compose port notes 80)"
printf '\nDeployment completed successfully.\n'
printf 'Open http://%s in your browser.\n' "${published_address}"
