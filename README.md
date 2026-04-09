# tab-pipeline

A staged audio processing pipeline for bass and guitar stem separation.

## What it does

`tab-pipeline` takes audio files as input and produces separated bass and guitar stems through a series of inspectable stages:

1. **Ingest** — Validate input, compute file hash, record metadata
2. **Normalize** — Convert to a canonical mono WAV using ffmpeg
3. **Separate** — Extract bass and guitar stems (pluggable backend: `stub` or `audio_separator`)

Each run creates a timestamped workspace under `data/runs/` with manifests and output stems.

## Quick start

### Requirements

- Python 3.11
- `uv` — dependency manager
- `ffmpeg` and `ffprobe`

### Installation

```bash
# Install uv (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install ffmpeg (macOS)
brew install ffmpeg

# Clone and sync dependencies
git clone https://github.com/ryanclarkdev/tab-pipeline.git
cd tab-pipeline
uv sync --extra dev
```

### Run a test

```bash
# Generate a test audio file
mkdir -p scratch
ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t 1 scratch/test.wav -y

# Run the default pipeline (stub backend)
uv run tab-pipeline run scratch/test.wav

# Run with real audio-separator backend
uv run tab-pipeline run scratch/test.wav --config configs/local-audio-separator.yaml
```

### Test suite

```bash
uv run pytest
```

## Output

Each run produces a timestamped directory under `data/runs/`:

```
data/runs/<run-id>/
  run.json                    # Run manifest and metadata
  workspace/
    normalize/
      normalized.wav          # Canonical mono file
    separate/
      bass.wav               # Separated bass stem
      guitar.wav             # Separated guitar stem
```

The manifest (`run.json`) includes:
- Run ID, creation time
- Input file metadata and hash
- Effective config snapshot
- Stage records with timing and artifact details

## Configuration

The project uses layered configs:
- **Packaged defaults**: `src/tab_pipeline/config/defaults.yaml`
- **Local overrides**: `configs/*.yaml` (passed via `--config` flag)

### Default settings

```yaml
pipeline:
  instrument: bass

normalize:
  sample_rate: 44100
  channels: 1
  codec: pcm_s16le

separation:
  backend: stub
  requested_stems:
    - bass
    - guitar
  model_filename: htdemucs_6s.yaml
  model_file_dir: data/models/audio-separator
```

## Backends

**Stub backend** (default)
- Fast, deterministic, useful for testing structure and validation
- Generates empty stems matching expected output structure

**Audio-separator backend**
- Real stem separation using the htdemucs model
- Requires model files in `data/models/audio-separator/`
- Activated via `--config configs/local-audio-separator.yaml`

## Project structure

```
tab-pipeline/
  src/tab_pipeline/
    cli.py                 # Command-line entrypoint
    config.py              # Config loading and validation
    constants.py           # Project-level paths and directories
    
    config/                # Packaged defaults
    core/                  # Core utilities (hashing, manifest, paths, runner)
    models/                # Data models (config, context, run)
    stages/                # Pipeline stages (ingest, normalize, separate)
    adapters/              # Backend implementations
  
  configs/                 # Local override configs
  data/
    inputs/                # Source audio files
    runs/                  # Run outputs (git-ignored)
    models/                # Model files
  
  tests/                   # Test suite
```

## Design

The project prioritizes:

- **Inspectable outputs** — Every run creates a timestamped workspace with full manifests
- **Pluggable backends** — Swap implementations for separation without changing core logic
- **Staged processing** — Each step (ingest → normalize → separate) is independent and auditable
- **Typed configuration** — Pydantic models with YAML defaults and runtime overrides

## Notes

- **Input files must be valid audio** — the pipeline invokes ffmpeg during normalization
- **Generated outputs are local** — `data/runs/` and `data/models/` are git-ignored
- **Tests use the stub backend** — keeping them lightweight and deterministic

