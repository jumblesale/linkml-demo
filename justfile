default:
    @just --list

generate: && db-clear
    uv run python generate/schema.py

db-clear:
    uv run python -m app.database --clear

test:
    uv run pytest

run:
    uv run uvicorn app.app:fast_api --reload

rerun: db-clear run