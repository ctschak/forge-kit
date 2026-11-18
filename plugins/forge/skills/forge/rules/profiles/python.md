# Profile: Python

Loaded when detection returns `python`. Existing tools in `pyproject.toml` / CI win (`rules/quality.md` QG4, QG5).

| Kind | Prefer existing | Default if absent (propose, QG5) |
|---|---|---|
| lint + format | Ruff / flake8 / black config | Ruff (`ruff check`, `ruff format --check`) |
| type | mypy / pyright config | mypy on changed packages, strictness matching the codebase |
| test | pytest / unittest | keep the runner already used (unittest stays unittest) |
| coverage | coverage.py / pytest-cov | coverage.py for changed-line check (QG6) |
| env | venv / uv / poetry / pip-tools | isolated venv; never install into system Python |

| ID | Check |
|---|---|
| PY1 | Exceptions: specific types caught; re-raise with context (`raise X(...) from e`); no bare `except:` (CS4). |
| PY2 | Typing: public functions annotated; `Any` only at untyped boundaries; dataclasses/TypedDict/pydantic for structured data. |
| PY3 | Resources: files, connections, locks via context managers; async resources closed; no blocking I/O inside `async def`. |
| PY4 | Input: validated at boundary (pydantic / explicit checks); SQL parameterized (SEC4); no `eval`/`pickle` on untrusted data. |
| PY5 | Dependencies: pinned in the project's lock/requirements file; new dep justified; no duplicate. |
| PY6 | Time + money: timezone-aware datetimes; `Decimal` or integer minor units for money. |
