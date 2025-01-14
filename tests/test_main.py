import os
import tempfile
from pathlib import Path

import pytest
from typer.testing import CliRunner

from lfp.main import app

runner = CliRunner()


@pytest.mark.parametrize(
    "database,frontend,tailwind,docker_dev,docker_prod",
    [
        ("sqlite", "vue", True, True, True),
        ("sqlite", "react", True, True, True),
        ("sqlite", "svelte", True, True, True),
        # ("sqlite", "htmx", True, True, True),  # htmx not supported yet
        ("postgresql", "vue", True, True, True),
        ("postgresql", "react", True, True, True),
        ("postgresql", "svelte", True, True, True),
        # ("postgresql", "htmx", True, True, True),  # htmx not supported yet
        ("sqlite", "vue", False, True, True),
        ("sqlite", "vue", True, False, True),
        ("sqlite", "vue", True, True, False),
        ("postgresql", "vue", False, False, False),
    ],
)
def test_new_project_with_options(
    database, frontend, tailwind, docker_dev, docker_prod
):
    """Test project creation using command line options"""
    with tempfile.TemporaryDirectory() as tmpdir:
        original_dir = Path.cwd()
        try:
            os.chdir(tmpdir)
            result = runner.invoke(
                app,
                [
                    "new",
                    "test_project",
                    "--database",
                    database,
                    "--frontend",
                    frontend,
                    "--tailwind" if tailwind else "--no-tailwind",
                    "--docker-in-dev" if docker_dev else "--no-docker-in-dev",
                    "--docker-in-prod"
                    if docker_prod
                    else "--no-docker-in-prod",
                ],
            )
            assert result.exit_code == 0
        finally:
            os.chdir(original_dir)


def test_htmx_frontend():
    """Test that htmx frontend is not supported yet"""
    result = runner.invoke(
        app,
        [
            "new",
            "test_project",
            "--database",
            "sqlite",
            "--frontend",
            "htmx",
            "--no-tailwind",
            "--no-docker-in-dev",
            "--no-docker-in-prod",
        ],
    )
    assert result.exit_code == 1
    assert "Frontend not supported yet" in result.stdout
