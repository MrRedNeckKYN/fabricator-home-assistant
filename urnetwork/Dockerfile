# Official provider image: published for amd64 and arm64. The g4 service block
# is documented upstream as the longest-tested/stablest rolling provider line.
FROM bringyour/community-provider:g4-latest

USER root
RUN mkdir -p /data/.urnetwork \
    && rm -rf /root/.urnetwork \
    && ln -s /data/.urnetwork /root/.urnetwork

COPY run.sh /usr/local/bin/ha-urnetwork-run
RUN chmod 0755 /usr/local/bin/ha-urnetwork-run

ENTRYPOINT ["/usr/local/bin/ha-urnetwork-run"]
