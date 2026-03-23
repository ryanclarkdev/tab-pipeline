from pathlib import Path
import shutil


def clear_run_directories(runs_dir: Path) -> int:
  removed = 0

  if not runs_dir.exists():
    return removed

  for child in runs_dir.iterdir():
    if child.name == ".gitkeep":
      continue

    if child.is_dir():
      shutil.rmtree(child)
      removed += 1
    elif child.is_file():
      child.unlink()
      removed += 1

  return removed