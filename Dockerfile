FROM python:3.12-slim

WORKDIR /app


RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


COPY pyproject.toml uv.lock* ./


RUN pip install --no-cache-dir uv && \
    uv sync --frozen


COPY . .

EXPOSE 8080

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]












