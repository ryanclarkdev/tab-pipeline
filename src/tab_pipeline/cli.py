from pathlib import Path

import typer

from tab_pipeline.core.cleanup import clear_run_directories
from tab_pipeline.core.runner import bootstrap_run
from tab_pipeline.paths import RUNS_DIR

app = typer.Typer(
  help="Local staged audio-to-tab pipeline.",
  no_args_is_help=True,
)


@app.callback()
def main() -> None:
  """
  Local staged audio-to-tab pipeline.
  """
  return None


@app.command()
def run(
  input_path: Path,
  config: Path | None = typer.Option(
    None,
    "--config",
    "-c",
    help="Optional path to a YAML config override file.",
  ),
) -> None:
  """
  Register and execute a pipeline run for an input audio file.
  """
  run_dir = bootstrap_run(input_path=input_path, config_path=config)
  typer.echo(f"Run created: {run_dir}")


@app.command("clean-runs")
def clean_runs(
  yes: bool = typer.Option(
    False,
    "--yes",
    "-y",
    help="Delete run directories without prompting.",
  ),
) -> None:
  """
  Remove generated run directories under data/runs.
  """
  if not yes:
    confirmed = typer.confirm(
      f"Delete all run artifacts under {RUNS_DIR}?"
    )
    if not confirmed:
      typer.echo("Aborted.")
      raise typer.Exit()

  removed = clear_run_directories(RUNS_DIR)
  typer.echo(f"Removed {removed} run artifact(s).")


if __name__ == "__main__":
  app()