from datetime import UTC, datetime
from pathlib import Path

from tab_pipeline.models.run import StageRecord


def separate_bass_stem(
  input_path: Path,
  output_path: Path,
  separator_name: str,
  separate_fn,
) -> StageRecord:
  started_at = datetime.now(UTC)

  output_path.parent.mkdir(parents=True, exist_ok=True)
  separate_fn(input_path, output_path)

  size_bytes = output_path.stat().st_size
  finished_at = datetime.now(UTC)

  return StageRecord(
    name="separate",
    status="completed",
    started_at=started_at,
    finished_at=finished_at,
    details={
      "separator": separator_name,
      "target": "bass",
      "output_path": str(output_path.resolve()),
      "size_bytes": size_bytes,
    },
  )