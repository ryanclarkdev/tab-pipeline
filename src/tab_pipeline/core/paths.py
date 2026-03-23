from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RunPaths:
  run_dir: Path

  @property
  def manifest_path(self) -> Path:
    return self.run_dir / "run.json"

  @property
  def workspace_dir(self) -> Path:
    return self.run_dir / "workspace"

  @property
  def normalize_dir(self) -> Path:
    return self.workspace_dir / "normalize"

  @property
  def normalized_audio_path(self) -> Path:
    return self.normalize_dir / "normalized.wav"

  @property
  def separate_dir(self) -> Path:
    return self.workspace_dir / "separate"

  @property
  def bass_stem_path(self) -> Path:
    return self.separate_dir / "bass.wav"