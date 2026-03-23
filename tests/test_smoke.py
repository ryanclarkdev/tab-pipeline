import json
import wave

from tab_pipeline.core.runner import bootstrap_run


def test_bootstrap_run(tmp_path, monkeypatch) -> None:
  input_file = tmp_path / "example.wav"

  with wave.open(str(input_file), "wb") as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(44100)
    wav_file.writeframes(b"\x00\x00" * 4410)

  runs_dir = tmp_path / "runs"

  monkeypatch.setattr("tab_pipeline.paths.RUNS_DIR", runs_dir)
  monkeypatch.setattr("tab_pipeline.core.runner.RUNS_DIR", runs_dir)

  config_file = tmp_path / "test-config.yaml"
  config_file.write_text(
    '''
  separation:
    backend: stub
  '''.strip(),
    encoding="utf-8",
  )

  run_dir = bootstrap_run(input_file, config_path=config_file)
  
  assert run_dir.exists()

  manifest_path = run_dir / "run.json"
  assert manifest_path.exists()

  manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

  assert manifest["input"]["source_name"] == "example.wav"
  assert manifest["config"]["normalize"]["sample_rate"] == 44100
  assert manifest["config"]["separation"]["backend"] == "stub"
  assert manifest["stages"][0]["name"] == "ingest"
  assert manifest["stages"][1]["name"] == "normalize"
  assert manifest["stages"][2]["name"] == "separate"
  assert manifest["stages"][2]["status"] == "completed"

  normalized_path = run_dir / "workspace" / "normalize" / "normalized.wav"
  bass_stem_path = run_dir / "workspace" / "separate" / "bass.wav"

  assert normalized_path.exists()
  assert bass_stem_path.exists()