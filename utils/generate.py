import os
from pathlib import Path
from typing import Optional

import typer
from cookiecutter.main import cookiecutter

app = typer.Typer()


@app.command()
def new_module(
    overwrite_if_exists: bool = typer.Option(False, help="Allow to overwrite the output directory if already exist"),
    config_file: Optional[Path] = typer.Option(None, help="User configuration file path"),
):
    current_dir = Path(os.path.dirname(__file__)).resolve()
    template = current_dir / "new_module"
    cookiecutter(
        template.as_posix(),
        overwrite_if_exists=overwrite_if_exists,
        config_file=config_file,
        output_dir=current_dir.parent.as_posix(),
    )


@app.command()
def new_format(
    module_dir: Path = typer.Argument(..., exists=True, dir_okay=True),
    overwrite_if_exists: bool = typer.Option(False, help="Allow to overwrite the output directory if already exist"),
    config_file: Optional[Path] = typer.Option(None, help="User configuration file path"),
):
    current_dir = Path(os.path.dirname(__file__)).resolve()
    module_dir = module_dir.resolve()

    if not module_dir.is_relative_to(current_dir.parent):
        typer.echo("The module is located outside the repository")
        raise typer.Exit(code=1)

    module_manifest = module_dir / "_meta" / "manifest.yml"
    if not module_manifest.exists():
        typer.echo("No manifest found in the module. Please ensure to select an existing module.")
        raise typer.Exit(code=2)

    template = current_dir / "new_intake"
    cookiecutter(
        template.as_posix(),
        overwrite_if_exists=overwrite_if_exists,
        config_file=config_file,
        output_dir=module_dir.as_posix(),
    )


if __name__ == "__main__":
    app()
