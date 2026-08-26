FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim

WORKDIR /backend
COPY . .

RUN uv sync --group tests

CMD ["uv", "run", "--group", "tests", "pytest"]