FROM python:3.12
COPY --from=ghcr.io/astral-sh/uv:0.3.3 /uv /bin/uv

WORKDIR /app/
COPY . /app/
RUN uv sync --frozen --no-install-project --no-dev
# todo get this from source control
RUN mv cosmic-theme-tools /usr/bin
RUN chmod a+x /usr/bin/cosmic-theme-tools

CMD uv run gunicorn cosmic_themes.wsgi --workers 2 --bind 0.0.0.0:8000
