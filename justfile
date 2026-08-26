default:
    @just --list

generate:
    python generate/schema.py

run:
    uv run uvicorn app.app:fast_api --reload
