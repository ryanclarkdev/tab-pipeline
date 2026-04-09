import json
import subprocess
from pathlib import Path
from typing import Any


def _run(command: list[str]) -> subprocess.CompletedProcess:
  try:
    return subprocess.run(command, check=True, capture_output=True, text=True)
  except FileNotFoundError as exc:
    raise RuntimeError(
      f"Required executable not found: {command[0]}. Is ffmpeg/ffprobe installed?"
    ) from exc
  except subprocess.CalledProcessError as exc:
    raise RuntimeError(
      f"Command failed: {' '.join(command)}\n"
      f"stdout:\n{exc.stdout}\n"
      f"stderr:\n{exc.stderr}"
    ) from exc


def run_ffmpeg_normalize(
  input_path: Path,
  output_path: Path,
  sample_rate: int = 44100,
  channels: int = 1,
) -> None:
  command = [
    "ffmpeg",
    "-y",
    "-i",
    str(input_path),
    "-ar",
    str(sample_rate),
    "-ac",
    str(channels),
    "-c:a",
    "pcm_s16le",
    str(output_path),
  ]

  _run(command)


def probe_audio(path: Path) -> dict[str, Any]:
  command = [
    "ffprobe",
    "-v",
    "error",
    "-print_format",
    "json",
    "-show_format",
    "-show_streams",
    str(path),
  ]

  result = _run(command)
  return json.loads(result.stdout)