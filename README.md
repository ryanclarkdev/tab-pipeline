# tab-pipeline

Local Python pipeline for staged audio-to-tab transcription workflows.

## Overview

`tab-pipeline` is a local, CLI-first Python project for building a deterministic audio transcription pipeline in small, inspectable stages.

The long-term goal is to support workflows like:

- full-song audio input
- source separation
- instrument-focused transcription
- fretboard or tab mapping
- digital tab export

The current scope is intentionally narrower. Right now, the project establishes the pipeline foundation and implements the first stages needed for downstream work.

## Current scope

Implemented so far:

- bootstrap a local project workspace
- expose a CLI entrypoint
- create a per-run output directory
- write a run manifest
- ingest an input audio file
- normalize input audio into a canonical WAV format

Not implemented yet:

- source separation
- pitch or note transcription
- tab mapping
- MIDI or GP5 export
- persistent caching beyond the current initial structure

## Project goals

This project is being built around a few engineering principles:

- **stage-by-stage development** instead of one large script
- **inspectable outputs** so each step can be verified independently
- **deterministic behavior** driven by explicit inputs and config
- **clean filesystem boundaries** between inputs, runs, cache, and exports
- **CLI-first workflows** that are easy to automate, test, and evolve

## Requirements

### System dependencies

The project currently depends on:

- **Python 3.11**
- **uv** for Python environment and dependency management
- **ffmpeg**
- **ffprobe**

`ffprobe` is typically installed alongside `ffmpeg`.

### Verify installed tools

Run the following to confirm your environment is ready:

```bash
python3 --version
uv --version
ffmpeg -version
ffprobe -version
```

Expected Python version for this project:

```text
3.11
```

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_REPO_URL>
cd tab-pipeline
```

### 2. Install uv

#### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For other install methods, refer to the official uv documentation.

### 3. Install ffmpeg

#### macOS (Homebrew)

```bash
brew install ffmpeg
```

#### Ubuntu / Debian

```bash
sudo apt update
sudo apt install ffmpeg
```

#### Windows

Install `ffmpeg` using your preferred package manager or the official binaries, then ensure both `ffmpeg` and `ffprobe` are available on your `PATH`.

### 4. Sync project dependencies

```bash
uv sync --extra dev
```

This will create the local virtual environment and install runtime and development dependencies.

## Development setup

You can use `uv run ...` directly, which is the simplest workflow.

If you want to activate the environment manually:

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

## Usage

### Run the pipeline on an audio file

```bash
uv run tab-pipeline run path/to/song.wav
```

Example:

```bash
uv run tab-pipeline run /absolute/path/to/real-audio-file.wav
```

A successful run will create a new run directory under `data/runs/`.

## What a run currently does

At the current stage of development, a run performs the following actions:

1. validates the input path
2. computes input metadata during ingest
3. creates a run directory
4. writes a run manifest
5. normalizes the input audio into a canonical WAV

The normalized output is currently written into the run workspace for inspection and downstream use.

## Testing

Run the test suite with:

```bash
uv run pytest
```

## Repository layout

```text
tab-pipeline/
  pyproject.toml
  README.md
  .python-version

  src/
    tab_pipeline/
      cli.py
      config.py
      paths.py

      core/
        runner.py
        manifest.py
        hashing.py

      models/
        run.py

      stages/
        ingest.py
        normalize.py

      adapters/
        ffmpeg.py

  data/
    inputs/
    runs/
    cache/
    exports/

  tests/
```

## Directory conventions

### `data/inputs/`
Local source audio files. These should be treated as immutable inputs.

### `data/runs/`
Per-run execution directories. Each invocation of the pipeline creates a new run directory here.

### `data/cache/`
Reserved for future deterministic stage caching.

### `data/exports/`
Reserved for user-facing export artifacts.

## Run artifacts

A typical run currently produces:

- a `run.json` manifest
- a normalized WAV file inside the run workspace

Example shape:

```text
data/runs/<run-id>/
  run.json
  workspace/
    normalize/
      normalized.wav
```

## Current implementation notes

- The pipeline currently normalizes audio to a canonical WAV format using `ffmpeg`.
- The normalize stage currently targets a mono working file to support the initial bass-first workflow direction.
- Stage outputs are still simple and local to a run; richer artifact modeling will come later.
- The project is intentionally avoiding premature orchestration complexity at this stage.

## Design direction

The intended development order is:

1. bootstrap workspace and CLI
2. ingest stage
3. normalize stage
4. source separation
5. note transcription
6. cleanup and post-processing
7. fretboard mapping
8. digital tab export

This order is deliberate. The project should behave like a small deterministic build system for music artifacts rather than a loose sequence of scripts.

## Development notes

### Formatting and linting

Runtime and development dependencies are managed through `uv`, and lint/test tooling is installed through the dev dependency group.

If configured in the current project version, you can run linting with:

```bash
uv run ruff check .
```

### Running from the project root

All commands in this README assume you are in the repository root:

```bash
cd tab-pipeline
```

## Git and local artifacts

The project ignores generated runtime artifacts under `data/` except for placeholder files used to preserve the directory structure.

Typical ignored runtime outputs include:

- run directories
- normalized audio outputs
- future cache artifacts
- local scratch files

## Near-term next steps

Planned next steps include:

- improving run and stage structure
- formalizing stage output paths
- adding source separation
- introducing more explicit artifact metadata
- evolving toward retriable and cacheable stage execution
