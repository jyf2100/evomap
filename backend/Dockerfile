FROM python:3.11-slim

WORKDIR /app

# Install uv using the official installer
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files
COPY pyproject.toml .
COPY README.md .
COPY uv.lock .
COPY alembic.ini .
COPY alembic ./alembic
COPY app ./app

# Install dependencies with no proxy (cache them in the image)
RUN HTTP_PROXY= HTTPS_PROXY= http_proxy= https_proxy= NO_PROXY=* uv sync --frozen --no-dev --cache-dir /root/.cache/uv

# Expose port
EXPOSE 8000

# Run migrations and start the application (use cached deps)
CMD ["sh", "-c", "HTTP_PROXY= HTTPS_PROXY= http_proxy= https_proxy= uv run --offline alembic upgrade head && uv run --offline uvicorn app.main:app --host 0.0.0.0 --port 8000"]
