.PHONY: run

run:
	uv run uvicorn main:app --host 0.0.0.0 --port 8080 --reload

test:
	uv run pytest -v

lint:
	uv run ruff check .

fix:
	uv run ruff check --fix .
