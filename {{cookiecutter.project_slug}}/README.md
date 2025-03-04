# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Installation

```bash
pip install -e .
```

## Usage

Run the server in SSE mode:

```bash
{{ cookiecutter.project_slug }}-server --port {{ cookiecutter.server_port }}
```

The server provides the following MCP tools:

- `echo`: A simple tool that echoes back the input text
