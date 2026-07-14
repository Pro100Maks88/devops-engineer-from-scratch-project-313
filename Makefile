.PHONY: run run-local test lint fix clean dev

run-local:
	DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/mydb" \
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload


run:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

test:
	docker compose run --rm \
		-e DATABASE_URL="postgresql+psycopg2://user:password@db:5432/mydb" \
		app uv run pytest -v

lint:
	uv run ruff check .

fix:
	uv run ruff check --fix .

clean:
	docker compose down -v
	rm -f uv.lock

dev:
	docker compose up -d


