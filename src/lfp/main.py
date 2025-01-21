import typer

from .new import app as new_app

app = typer.Typer(no_args_is_help=True)


@app.callback()
def callback():
    """
    The battery pack for your Django projects
    """


app.add_typer(new_app)
