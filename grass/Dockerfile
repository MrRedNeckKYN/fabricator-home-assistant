FROM mrcolorrain/vnc-browser:debian

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends chromium chromium-driver python3-requests python3-selenium; \
    rm -rf /var/lib/apt/lists/*

# vnc-browser invokes executable scripts here when CUSTOMIZE=true.
COPY grass_node.py /app/custom_entrypoints_scripts/10-grass-node.py
RUN chmod 0755 /app/custom_entrypoints_scripts/10-grass-node.py

ENV CUSTOMIZE=true \
    AUTO_START_BROWSER=false \
    AUTO_START_XTERM=false
