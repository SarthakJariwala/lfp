import os
from pathlib import Path

import copier
import questionary
import typer
from rich.status import Status

app = typer.Typer(no_args_is_help=True)


@app.callback()
def callback():
    """
    The battery pack for your Django projects
    """


@app.command(name="new")
def new(project_name: str = typer.Argument(None, help="Your project name")):
    """
    Create a new Django project with battery pack configured
    """
    if not project_name:
        project_name = questionary.text("Your project name").ask()
        if not project_name:  # Immediately exit if still empty
            typer.echo("Project name cannot be empty")
            raise typer.Exit(1)
    project_name = project_name.lower().replace(" ", "_").replace("-", "_")
    database: str = questionary.select(
        "Which database do you want to use?", default="sqlite", choices=["sqlite", "postgresql"]
    ).ask()
    frontend: str = questionary.select(
        "Which frontend do you want to use?", choices=["htmx", "vue", "react", "svelte"], default="vue"
    ).ask()
    tailwind: bool = questionary.confirm("Do you want to use Tailwind CSS?", default=True).ask()
    docker_in_dev: bool = questionary.confirm("Do you want to use Docker in development?", default=True).ask()
    docker_in_prod: bool = questionary.confirm("Do you want to use Docker in production?", default=True).ask()

    if frontend == "vue":
        src_path = "gh:SarthakJariwala/django-vite-inertia"
    else:
        typer.echo("Frontend not supported yet")
        raise typer.Exit(1)

    data = {
        "project_name": project_name,
        "database": database,
        "frontend": frontend,
        "tailwind_css": tailwind,
        "docker_dev": docker_in_dev,
        "docker_prod": docker_in_prod,
    }
    with Status(f"Creating project {project_name}..."):
        project_path = Path(project_name)
        os.makedirs(project_path, exist_ok=True)
        with copier.Worker(src_path=src_path, dst_path=project_path, data=data) as worker:
            worker.run_copy()
