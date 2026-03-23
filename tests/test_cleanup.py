from tab_pipeline.core.cleanup import clear_run_directories


def test_clear_run_directories(tmp_path) -> None:
  runs_dir = tmp_path / "runs"
  runs_dir.mkdir()

  keep_file = runs_dir / ".gitkeep"
  keep_file.write_text("", encoding="utf-8")

  run_a = runs_dir / "run-a"
  run_a.mkdir()
  (run_a / "run.json").write_text("{}", encoding="utf-8")

  run_b = runs_dir / "run-b"
  run_b.mkdir()
  (run_b / "run.json").write_text("{}", encoding="utf-8")

  removed = clear_run_directories(runs_dir)

  assert removed == 2
  assert keep_file.exists()
  assert not run_a.exists()
  assert not run_b.exists()