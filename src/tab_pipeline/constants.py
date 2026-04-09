from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
INPUTS_DIR = DATA_DIR / "inputs"
RUNS_DIR = DATA_DIR / "runs"
CACHE_DIR = DATA_DIR / "cache"
EXPORTS_DIR = DATA_DIR / "exports"


def ensure_directories() -> None:
  for path in (INPUTS_DIR, RUNS_DIR, CACHE_DIR, EXPORTS_DIR):
    path.mkdir(parents=True, exist_ok=True)