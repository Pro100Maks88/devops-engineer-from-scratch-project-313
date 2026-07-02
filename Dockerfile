FROM python:3.12-slim

RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

COPY nginx.conf /etc/nginx/conf.d/default.conf


COPY pyproject.toml uv.lock ./


RUN pip install uv
RUN uv sync --frozen

RUN pip install \
    "fastapi>=0.137.1" \
    "uvicorn>=0.49.0" \
    "sqlmodel>=0.0.38" \
    "psycopg2-binary>=2.9.12" \
    "sentry-sdk>=2.63.0" \
    "python-dotenv>=1.0.1"


COPY app/ ./app/
COPY public ./public

EXPOSE 80

CMD sh -c "nginx && exec uvicorn app.main:app --host 0.0.0.0 --port 8080"




