import json

from tab_pipeline.core.runner import bootstrap_run


def test_bootstrap_run(tmp_path, monkeypatch) -> None:
  input_file = tmp_path / "example.wav"
  input_file.write_bytes(b"fake-audio")

  runs_dir = tmp_path / "runs"

  monkeypatch.setattr("tab_pipeline.paths.RUNS_DIR", runs_dir)
  monkeypatch.setattr("tab_pipeline.core.runner.RUNS_DIR", runs_dir)

  run_dir = bootstrap_run(input_file)

  assert run_dir.exists()

  manifest_path = run_dir / "run.json"
  assert manifest_path.exists()

  manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

  assert manifest["input"]["source_name"] == "example.wav"
  assert manifest["input"]["size_bytes"] == len(b"fake-audio")
  assert manifest["input"]["sha256"]
  assert manifest["stages"][0]["name"] == "ingest"
  assert manifest["stages"][0]["status"] == "completed"