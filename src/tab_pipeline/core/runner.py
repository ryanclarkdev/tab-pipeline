from datetime import UTC, datetime
from pathlib import Path

from tab_pipeline.adapters.audio_separator_backend import AudioSeparatorBackend
from tab_pipeline.adapters.stub_separator import StubSeparator
from tab_pipeline.config import load_config
from tab_pipeline.core.manifest import write_manifest
from tab_pipeline.core.paths import RunPaths
from tab_pipeline.models.config import PipelineConfig
from tab_pipeline.models.context import RunContext
from tab_pipeline.models.run import RunManifest
from tab_pipeline.paths import ROOT_DIR, RUNS_DIR, ensure_directories
from tab_pipeline.stages.ingest import ingest_input
from tab_pipeline.stages.normalize import normalize_audio
from tab_pipeline.stages.separate import separate_bass_stem


def _build_run_id() -> str:
  timestamp = datetime.now(UTC).strftime("%Y-%m-%dT%H-%M-%SZ")
  return timestamp


def _create_run_context(config: PipelineConfig) -> RunContext:
  run_id = _build_run_id()
  run_dir = RUNS_DIR / run_id
  run_dir.mkdir(parents=True, exist_ok=False)

  return RunContext(
    run_id=run_id,
    paths=RunPaths(run_dir=run_dir),
    config=config,
  )


def _build_separator(ctx: RunContext):
  backend = ctx.config.separation.backend

  if backend == "stub":
    return StubSeparator()

  if backend == "audio_separator":
    model_dir = Path(ctx.config.separation.model_file_dir)
    if not model_dir.is_absolute():
      model_dir = ROOT_DIR / model_dir

    return AudioSeparatorBackend(
      model_filename=ctx.config.separation.model_filename,
      model_file_dir=model_dir,
      sample_rate=ctx.config.normalize.sample_rate,
    )

  raise ValueError(f"Unsupported separation backend: {backend}")


def bootstrap_run(input_path: Path, config_path: Path | None = None) -> Path:
  ensure_directories()

  config = load_config(config_path)
  ctx = _create_run_context(config)

  run_input, ingest_stage = ingest_input(input_path)

  normalize_stage = normalize_audio(
    input_path=Path(run_input.source_path),
    output_path=ctx.paths.normalized_audio_path,
    sample_rate=ctx.config.normalize.sample_rate,
    channels=ctx.config.normalize.channels,
  )

  separator = _build_separator(ctx)

  separate_stage = separate_bass_stem(
    input_path=ctx.paths.normalized_audio_path,
    output_path=ctx.paths.bass_stem_path,
    separator_name=separator.name,
    separate_fn=separator.separate_bass,
  )

  manifest = RunManifest(
    run_id=ctx.run_id,
    config=ctx.config.model_dump(mode="python"),
    input=run_input,
    stages=[ingest_stage, normalize_stage, separate_stage],
  )

  write_manifest(ctx.paths.manifest_path, manifest)

  return ctx.paths.run_dir