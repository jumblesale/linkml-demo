default:
    @just --list

run:
    uv run uvicorn app.app:fast_api --reload
