FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim
WORKDIR /backend
COPY . .
RUN uv sync
EXPOSE 8000
CMD ["uv", "run", "fastapi", "run", "server.py", "--host", "0.0.0.0"]
