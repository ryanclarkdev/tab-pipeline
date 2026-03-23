from datetime import UTC, datetime
from pathlib import Path

from tab_pipeline.core.manifest import write_manifest
from tab_pipeline.models.run import RunManifest
from tab_pipeline.paths import RUNS_DIR, ensure_directories
from tab_pipeline.stages.ingest import ingest_input
from tab_pipeline.stages.normalize import normalize_audio


def _build_run_id() -> str:
  timestamp = datetime.now(UTC).strftime("%Y-%m-%dT%H-%M-%SZ")
  return timestamp


def bootstrap_run(input_path: Path) -> Path:
  ensure_directories()

  run_id = _build_run_id()
  run_dir = RUNS_DIR / run_id
  run_dir.mkdir(parents=True, exist_ok=False)

  run_input, ingest_stage = ingest_input(input_path)

  normalized_dir = run_dir / "workspace" / "normalize"
  normalized_path = normalized_dir / "normalized.wav"

  normalize_stage = normalize_audio(
    input_path=Path(run_input.source_path),
    output_path=normalized_path,
    sample_rate=44100,
    channels=1,
  )

  manifest = RunManifest(
    run_id=run_id,
    input=run_input,
    stages=[ingest_stage, normalize_stage],
  )

  write_manifest(run_dir / "run.json", manifest)

  return run_dir