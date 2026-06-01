#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${CFA_NOTES_REPO_URL:-https://github.com/guai6mmt/CFA-notes.git}"
INSTALL_DIR="${CFA_NOTES_DIR:-${HOME}/CFA-notes}"

fail() {
  printf 'Error: %s\n' "$*" >&2
  exit 1
}

command -v git >/dev/null 2>&1 || fail "git is required. Install Git and run this command again."

if [[ -d "${INSTALL_DIR}/.git" ]]; then
  printf 'Using existing checkout: %s\n' "${INSTALL_DIR}"
elif [[ -e "${INSTALL_DIR}" ]]; then
  fail "${INSTALL_DIR} already exists but is not a Git checkout."
else
  printf 'Cloning notes site into %s\n' "${INSTALL_DIR}"
  git clone "${REPO_URL}" "${INSTALL_DIR}"
fi

if [[ -n "${NOTES_BIND_ADDRESS+x}" || -n "${NOTES_PORT+x}" ]]; then
  NOTES_BIND_ADDRESS="${NOTES_BIND_ADDRESS:-0.0.0.0}"
  NOTES_PORT="${NOTES_PORT:-8889}"

  [[ "${NOTES_PORT}" =~ ^[0-9]+$ ]] || fail "NOTES_PORT must be a number."
  (( NOTES_PORT >= 1 && NOTES_PORT <= 65535 )) || fail "NOTES_PORT must be between 1 and 65535."

  cat > "${INSTALL_DIR}/.env" <<EOF
NOTES_BIND_ADDRESS=${NOTES_BIND_ADDRESS}
NOTES_PORT=${NOTES_PORT}
EOF
  printf 'Saved deployment settings in %s/.env\n' "${INSTALL_DIR}"
fi

exec bash "${INSTALL_DIR}/scripts/deploy.sh"
