from datetime import UTC, datetime
from pathlib import Path

from tab_pipeline.core.hashing import sha256_file
from tab_pipeline.models.run import RunInput, StageRecord


def ingest_input(input_path: Path) -> tuple[RunInput, StageRecord]:
  started_at = datetime.now(UTC)

  if not input_path.exists():
    raise FileNotFoundError(f"Input file does not exist: {input_path}")

  if not input_path.is_file():
    raise ValueError(f"Input path is not a file: {input_path}")

  resolved_path = input_path.resolve()
  file_hash = sha256_file(resolved_path)
  size_bytes = resolved_path.stat().st_size

  run_input = RunInput(
    source_path=str(resolved_path),
    source_name=resolved_path.name,
    sha256=file_hash,
    size_bytes=size_bytes,
  )

  finished_at = datetime.now(UTC)

  stage_record = StageRecord(
    name="ingest",
    status="completed",
    started_at=started_at,
    finished_at=finished_at,
    details={
      "source_name": resolved_path.name,
      "size_bytes": size_bytes,
    },
  )

  return run_input, stage_record