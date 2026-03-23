from pathlib import Path

from audio_separator.separator import Separator


class AudioSeparatorBackend:
  name = "audio_separator"

  def __init__(
    self,
    model_filename: str,
    model_file_dir: Path,
    sample_rate: int = 44100,
  ) -> None:
    self.model_filename = model_filename
    self.model_file_dir = model_file_dir
    self.sample_rate = sample_rate

  def separate_bass(
    self,
    input_path: Path,
    output_path: Path,
  ) -> None:
    output_dir = output_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    self.model_file_dir.mkdir(parents=True, exist_ok=True)

    separator = Separator(
      output_dir=str(output_dir),
      model_file_dir=str(self.model_file_dir),
      output_single_stem="Bass",
      sample_rate=self.sample_rate,
    )

    separator.load_model(model_filename=self.model_filename)

    output_files = separator.separate(str(input_path))

    bass_file = self._resolve_bass_file(output_files, output_dir=output_dir)

    if bass_file.resolve() != output_path.resolve():
      bass_file.replace(output_path)

  @staticmethod
  def _resolve_bass_file(output_files: list[str], output_dir: Path) -> Path:
    candidates: list[Path] = []

    for value in output_files:
      path = Path(value)
      if not path.is_absolute():
        path = output_dir / path
      candidates.append(path)

    for path in candidates:
      if "bass" in path.name.lower():
        return path

    raise RuntimeError(
      f"Audio separator did not return a recognizable bass stem. Output files: {output_files}"
    )