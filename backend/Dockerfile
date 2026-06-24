FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim
WORKDIR /progetto2-fas
COPY pyproject.toml ./
COPY . .
RUN uv sync
RUN ls -la
EXPOSE 8000
CMD ["uv", "run","fastapi", "run", "server.py", "--host", "0.0.0.0"]