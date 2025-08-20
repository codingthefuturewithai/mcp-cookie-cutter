"""Test configuration for pytest."""

import os
import pytest


# Set coverage environment variable before any tests run
os.environ["COVERAGE_PROCESS_START"] = ".coveragerc"


@pytest.fixture(autouse=True)
def ensure_coverage_tracking():
    """Ensure coverage tracking is enabled for all tests."""
    # This fixture runs for every test, keeping the env var set
    assert os.environ.get("COVERAGE_PROCESS_START") == ".coveragerc"
    yield


@pytest.fixture
def anyio_backend():
    """Configure anyio to use asyncio backend."""
    return "asyncio"