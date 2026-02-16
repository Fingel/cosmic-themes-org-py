FROM node:23 as node_deps

WORKDIR /app/
COPY package.json package-lock.json /app/
RUN npm install

FROM python:3.14
COPY --from=ghcr.io/astral-sh/uv:0.10.2 /uv /bin/uv

WORKDIR /app/
COPY --from=node_deps /app/node_modules/ /app/node_modules/
COPY . /app/
RUN uv sync --frozen --no-dev
# todo get this from source control
RUN mv cosmic-theme-tools /usr/bin
RUN chmod a+x /usr/bin/cosmic-theme-tools

CMD uv run gunicorn cosmic_themes.wsgi --workers 2 --bind 0.0.0.0:8000
