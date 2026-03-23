from datetime import UTC, datetime
from pathlib import Path

from tab_pipeline.adapters.ffmpeg import probe_audio, run_ffmpeg_normalize
from tab_pipeline.models.run import StageRecord


def normalize_audio(
  input_path: Path,
  output_path: Path,
  sample_rate: int = 44100,
  channels: int = 1,
) -> StageRecord:
  started_at = datetime.now(UTC)

  output_path.parent.mkdir(parents=True, exist_ok=True)

  run_ffmpeg_normalize(
    input_path=input_path,
    output_path=output_path,
    sample_rate=sample_rate,
    channels=channels,
  )

  probe = probe_audio(output_path)
  audio_stream = next(
    (stream for stream in probe.get("streams", []) if stream.get("codec_type") == "audio"),
    None,
  )

  if audio_stream is None:
    raise ValueError(f"No audio stream found in normalized file: {output_path}")

  duration = probe.get("format", {}).get("duration")
  size_bytes = output_path.stat().st_size

  finished_at = datetime.now(UTC)

  return StageRecord(
    name="normalize",
    status="completed",
    started_at=started_at,
    finished_at=finished_at,
    details={
      "output_path": str(output_path.resolve()),
      "sample_rate": int(audio_stream["sample_rate"]),
      "channels": int(audio_stream["channels"]),
      "codec_name": audio_stream.get("codec_name"),
      "duration_seconds": float(duration) if duration is not None else None,
      "size_bytes": size_bytes,
    },
  )