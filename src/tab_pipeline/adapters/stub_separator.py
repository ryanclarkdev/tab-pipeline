import shutil
from pathlib import Path


class StubSeparator:
  name = "stub"

  def separate_bass(
    self,
    input_path: Path,
    output_path: Path,
  ) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(input_path, output_path)