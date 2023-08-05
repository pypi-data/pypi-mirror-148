import os
import subprocess

import typer

app = typer.Typer()


@app.command()
def sync():
    """
    Create new QGIS templates based on ArcPro templates
    """
    DEFAULTCMF = os.environ.get("DefaultCMF")
    ProPy = os.environ.get("ProPy")

    if not DEFAULTCMF:
        typer.echo("Please set the environment variable DefaultCMF")

    if not ProPy:
        typer.echo("Please set the environment variable ProPy")

    if DEFAULTCMF and ProPy:
        dirname = os.path.dirname(__file__)
        script = os.path.realpath(os.path.join(
            dirname, '..', '..', 'scripts', 'mapElementLocationsPro.py'
        ))
        typer.echo("--- Running Sync Templates Script ---")
        subprocess.call([ProPy, script])


if __name__ == "__main__":
    app()
