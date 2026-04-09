from datetime import UTC, datetime
from pathlib import Path

from tab_pipeline.adapters.separator import Separator
from tab_pipeline.models.run import StageRecord


def separate_stems(
  input_path: Path,
  output_dir: Path,
  requested_stems: list[str],
  separator: Separator,
) -> StageRecord:
  started_at = datetime.now(UTC)

  output_dir.mkdir(parents=True, exist_ok=True)
  outputs = separator.separate_stems(input_path, output_dir, requested_stems)

  details: dict[str, str | int | float | bool | None] = {
    "separator": separator.name,
    "requested_stem_count": len(requested_stems),
  }

  for stem in requested_stems:
    path = outputs.get(stem)
    if path is None:
      raise RuntimeError(f"Separator did not return requested stem: {stem}")

    details[f"{stem}_output_path"] = str(path.resolve())
    details[f"{stem}_size_bytes"] = path.stat().st_size

  finished_at = datetime.now(UTC)

  return StageRecord(
    name="separate",
    status="completed",
    started_at=started_at,
    finished_at=finished_at,
    details=details,
  )