from pathlib import Path
from typing import Protocol


class Separator(Protocol):
  name: str

  def separate_bass(
    self,
    input_path: Path,
    output_path: Path,
  ) -> None:
    ...