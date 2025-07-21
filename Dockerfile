FROM python:3.11.2

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UV_PROJECT_ENVIRONMENT="/.venv/"

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.7.8 /uv /uvx /bin/

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

COPY . .

RUN chmod +x ./infra/commands/*.sh