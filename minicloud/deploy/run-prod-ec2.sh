#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)

cd "$REPO_ROOT"

if [ ! -f .env ]; then
  if [ -f .env.example ]; then
    cp .env.example .env
    echo "Created .env from .env.example. Update DOCKERHUB_NAMESPACE if needed."
  else
    echo "Create .env with DOCKERHUB_NAMESPACE and IMAGE_TAG before running production deploy." >&2
    exit 1
  fi
fi

docker compose -f docker-compose.prod.yml --env-file .env pull
docker compose -f docker-compose.prod.yml --env-file .env config >/dev/null
docker compose -f docker-compose.prod.yml --env-file .env up -d
