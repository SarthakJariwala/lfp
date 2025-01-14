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

            project_path = Path(tmpdir) / "test_project"

            assert project_path.exists()
            assert project_path.is_dir()

            assert (project_path / "manage.py").exists()
            assert (project_path / "manage.py").is_file()
            assert (project_path / "test_project").exists()
            assert (project_path / "test_project").is_dir()
            assert (project_path / "test_project" / "settings.py").exists()
            assert (project_path / "test_project" / "settings.py").is_file()

            assert (project_path / "src").exists()
            assert (project_path / "src").is_dir()
            assert (project_path / "src" / "js").exists()
            assert (project_path / "src" / "js").is_dir()
            assert (project_path / "src" / "css").exists()
            assert (project_path / "src" / "css").is_dir()

            if frontend == "react":
                assert (project_path / "src" / "js" / "main.jsx").exists()
                assert (project_path / "src" / "js" / "main.jsx").is_file()
            else:
                assert (project_path / "src" / "js" / "main.js").exists()
                assert (project_path / "src" / "js" / "main.js").is_file()

            if tailwind:
                tailwind_config_path = project_path / "tailwind.config.js"
                postcss_config_path = project_path / "postcss.config.js"
                assert tailwind_config_path.exists()
                assert tailwind_config_path.is_file()
                assert postcss_config_path.exists()
                assert postcss_config_path.is_file()

            if docker_dev:
                assert (project_path / "dev.Dockerfile").exists()
                assert (project_path / "dev.Dockerfile").is_file()
                assert (project_path / "docker-compose.yaml").exists()
                assert (project_path / "docker-compose.yaml").is_file()
            if docker_prod:
                assert (project_path / "prod.Dockerfile").exists()
                assert (project_path / "prod.Dockerfile").is_file()
                assert (project_path / "docker_startup.sh").exists()
                assert (project_path / "docker_startup.sh").is_file()
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
