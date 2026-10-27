FROM docker.io/searxng/searxng@sha256:aecad882e86eeb022b76351c8dce4eb48d0cbb16a5f1691f77ea32c96d317502
USER root
COPY . /opt/altstack-search/
COPY assets/logo.svg /opt/altstack-search/logo.svg
RUN /usr/local/searxng/.venv/bin/python /opt/altstack-search/brand.py && cd /opt/altstack-search && /usr/local/searxng/.venv/bin/python -m unittest discover -s tests && /usr/local/searxng/.venv/bin/python -m compileall -q -f /usr/local/searxng/searx && mkdir -p /etc/searxng /var/cache/searxng && chown -R 977:977 /etc/searxng /var/cache/searxng /opt/altstack-search
USER 977:977
ENV SEARXNG_SETTINGS_PATH=/etc/searxng/settings.yml SEARXNG_PORT=8080
LABEL org.opencontainers.image.title="Cohnsoft Search" org.opencontainers.image.licenses="AGPL-3.0-or-later" org.opencontainers.image.source="https://github.com/danecohn/Artemisearch"
EXPOSE 8080
ENTRYPOINT ["/bin/sh","/opt/altstack-search/start.sh"]
