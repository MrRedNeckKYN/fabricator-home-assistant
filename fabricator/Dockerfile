# Fabricator publishes a multi-architecture image for amd64 and arm64.
# Keep this pinned: upgrades should be reviewed and made intentionally in
# config.yaml and this FROM line together.
FROM ghcr.io/philderks/fabricator:1.5.0

COPY run.sh /usr/local/bin/ha-fabricator-run
RUN chmod 0755 /usr/local/bin/ha-fabricator-run

# The upstream entrypoint fixes the /data mount ownership, drops privileges to
# the upstream `fabricator` user, and makes tini PID 1.  It then starts run.py.
ENTRYPOINT ["/usr/local/bin/ha-fabricator-run"]
