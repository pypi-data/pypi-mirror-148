from typing import Optional

import typer

import mapaction.modules.templates.templates
from mapaction.libs.version import getLatestPyPiVersion
from mapaction.libs.version import getVerison

app = typer.Typer()
app.add_typer(
    mapaction.modules.templates.templates.app,
    name="templates",
    help="Utils for managing the templates"
)


def _version_callback(value: bool) -> None:
    if value:
        __version__ = getVerison()
        typer.echo(f"v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )

) -> None:
    return


def run() -> None:
    """Run commands."""
    getLatestPyPiVersion()
    app()
