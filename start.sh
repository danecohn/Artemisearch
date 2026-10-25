#!/bin/sh
set -eu
test -n "${SEARXNG_SECRET:-}" || { echo 'SEARXNG_SECRET is required' >&2; exit 1; }
test -n "${SEARXNG_VALKEY_URL:-}" || { echo 'Search rate-limit storage is required' >&2; exit 1; }
mkdir -p /etc/searxng
cp /opt/altstack-search/settings.yml /etc/searxng/settings.yml
cp /opt/altstack-search/limiter.toml /etc/searxng/limiter.toml
export SEARXNG_PORT="${PORT:-8080}"
exec /usr/local/searxng/entrypoint.sh
