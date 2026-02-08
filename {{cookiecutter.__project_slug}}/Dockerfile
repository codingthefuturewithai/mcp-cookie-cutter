FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml ./
RUN uv venv /app/.venv && \
    uv pip install --python /app/.venv/bin/python -e . --no-cache-dir
COPY {{ cookiecutter.__project_slug }}/ ./{{ cookiecutter.__project_slug }}/

FROM python:3.12-slim AS runtime
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid 1000 --create-home appuser
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/{{ cookiecutter.__project_slug }} /app/{{ cookiecutter.__project_slug }}
COPY --from=builder /app/pyproject.toml /app/pyproject.toml
RUN mkdir -p /home/appuser/.{{ cookiecutter.__project_slug }} \
             /home/appuser/.config/{{ cookiecutter.__project_slug }} \
             /home/appuser/.local/share/{{ cookiecutter.__project_slug }} && \
    chown -R appuser:appuser /home/appuser /app
USER appuser
ENV PATH="/app/.venv/bin:$PATH" PYTHONPATH="/app" HOME="/home/appuser"
ENV LOG_LEVEL="INFO" PORT="{{ cookiecutter.server_port }}"
EXPOSE {{ cookiecutter.server_port }}
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import socket; s = socket.socket(); s.settimeout(5); s.connect(('127.0.0.1', {{ cookiecutter.server_port }})); s.close()"
CMD ["python", "-m", "{{ cookiecutter.__project_slug }}", "--transport", "streamable-http", "--host", "0.0.0.0", "--port", "{{ cookiecutter.server_port }}"]
