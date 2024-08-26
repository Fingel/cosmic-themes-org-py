FROM python:3.12
COPY --from=ghcr.io/astral-sh/uv:0.3.3 /uv /bin/uv

WORKDIR /app/
COPY . /app/
RUN uv sync --frozen --no-install-project --no-dev

CMD uv gunicorn cosmic_themes.wsgi --workers 2 --bind 0.0.0.0:8000
