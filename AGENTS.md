# AGENTS.md

This file applies to everything under `fastapi-template/`.

## Purpose

Treat this repository as the FastAPI project being built from this codebase. Prefer changes that keep the application coherent and preserve the current layered structure:

- `fastapi_app/app/routers/`: API layer
- `fastapi_app/app/dependencies.py`: dependency wiring
- `fastapi_app/app/business_logic/`: service layer
- `fastapi_app/app/sql/`: database layer

## Maintenance Rules

- This file is self-maintained. If you make changes that affect anything documented here, update `AGENTS.md` in the same change.
- If you change code, also update the relevant documentation in the same change. At minimum, review `README.md`, `docs/README.md`, `docs/bruno_collection/`, and `docs/uml/architecture.puml`.
- If you change environment variables, ports, startup commands, or container behavior, update `dot_env_example`, `compose.yml`, `.devcontainer/`, and `README.md` as needed.
- Keep examples, naming, and documentation aligned with the actual project domain and behavior implemented in this repository.
- When routes, payloads, or persistence models change, update the API examples and architecture docs so they reflect the current service rather than an earlier scaffold.

## Verification

- For Python code changes, run `python3 -m compileall fastapi_app/app`.
- If you edit shell or JSON files, validate them before finishing.
