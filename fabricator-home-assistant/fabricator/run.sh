#!/bin/sh
# Home Assistant stores app options here.  Convert only documented options to
# Fabricator environment variables; all server/world data remains in /data.
set -eu

OPTIONS_FILE=/data/options.json

if [ -f "$OPTIONS_FILE" ]; then
    export FABRICATOR_OPTIONS_FILE="$OPTIONS_FILE"
    eval "$(python3 - <<'PY'
import json
import os
import shlex

path = os.environ['FABRICATOR_OPTIONS_FILE']
with open(path, encoding='utf-8') as source:
    options = json.load(source)

mapping = {
    'secret_key': 'SECRET_KEY',
    'auth_password_hash': 'FABRICATOR_AUTH_PASSWORD_HASH',
}
for option, variable in mapping.items():
    value = options.get(option)
    if value:
        print(f'export {variable}={shlex.quote(str(value))}')

# This merely enables Fabricator's optional outbound playit.gg tunnel agent.
# It never opens an inbound dashboard port by itself.
if options.get('playit_enabled'):
    print('export PLAYIT_ENABLED=true')
PY
)"
fi

# Do not replace this with `python run.py`: the upstream entrypoint supplies
# mount ownership repair, privilege drop, tini signal forwarding, and PID 1.
exec /usr/local/bin/docker-entrypoint.sh python run.py
