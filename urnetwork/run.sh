#!/bin/sh
set -eu

STATE_DIR=/data/.urnetwork
mkdir -p "$STATE_DIR"

# On its first start, pair this provider with a short-lived auth code generated
# in the user's URnetwork account. Do not try again after credentials exist:
# the code is one-time/short-lived and does not need to stay in add-on options.
if [ -n "${auth_code:-}" ] && [ -z "$(find "$STATE_DIR" -mindepth 1 -print -quit)" ]; then
    echo "Pairing URnetwork provider with the supplied auth code..."
    /usr/local/sbin/bringyour-provider auth "$auth_code"
fi

if [ -z "$(find "$STATE_DIR" -mindepth 1 -print -quit)" ]; then
    echo "No saved URnetwork provider credentials. Generate an auth code at ur.io, add it to auth_code, then restart this add-on."
    exit 1
fi

unset auth_code
exec /usr/local/sbin/bringyour-provider provide
