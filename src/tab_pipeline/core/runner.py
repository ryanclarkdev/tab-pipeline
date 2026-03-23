from datetime import UTC, datetime
from pathlib import Path

from tab_pipeline.adapters.stub_separator import StubSeparator
from tab_pipeline.core.manifest import write_manifest
from tab_pipeline.core.paths import RunPaths
from tab_pipeline.models.context import RunContext
from tab_pipeline.models.run import RunManifest
from tab_pipeline.paths import RUNS_DIR, ensure_directories
from tab_pipeline.stages.ingest import ingest_input
from tab_pipeline.stages.normalize import normalize_audio
from tab_pipeline.stages.separate import separate_bass_stem


def _build_run_id() -> str:
  timestamp = datetime.now(UTC).strftime("%Y-%m-%dT%H-%M-%SZ")
  return timestamp


def _create_run_context() -> RunContext:
  run_id = _build_run_id()
  run_dir = RUNS_DIR / run_id
  run_dir.mkdir(parents=True, exist_ok=False)

  return RunContext(
    run_id=run_id,
    paths=RunPaths(run_dir=run_dir),
  )


def bootstrap_run(input_path: Path) -> Path:
  ensure_directories()

  ctx = _create_run_context()

  run_input, ingest_stage = ingest_input(input_path)

  normalize_stage = normalize_audio(
    input_path=Path(run_input.source_path),
    output_path=ctx.paths.normalized_audio_path,
    sample_rate=44100,
    channels=1,
  )

  separator = StubSeparator()

  separate_stage = separate_bass_stem(
    input_path=ctx.paths.normalized_audio_path,
    output_path=ctx.paths.bass_stem_path,
    separator_name=separator.name,
    separate_fn=separator.separate_bass,
  )

  manifest = RunManifest(
    run_id=ctx.run_id,
    input=run_input,
    stages=[ingest_stage, normalize_stage, separate_stage],
  )

  write_manifest(ctx.paths.manifest_path, manifest)

  return ctx.paths.run_dir