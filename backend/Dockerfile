FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim
WORKDIR /backend
COPY . .
RUN uv sync
RUN useradd --create-home backenduser
RUN chown -R backenduser:backenduser /backend
USER backenduser
EXPOSE 8000
#CMD ["uv", "run", "fastapi", "run", "server.py", "--host", "0.0.0.0"]
CMD ["uv", "run", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]