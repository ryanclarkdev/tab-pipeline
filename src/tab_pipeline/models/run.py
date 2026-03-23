from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, Field


class RunInput(BaseModel):
  source_path: str
  source_name: str
  sha256: str
  size_bytes: int


class StageRecord(BaseModel):
  name: str
  status: Literal["completed", "failed"]
  started_at: datetime
  finished_at: datetime
  details: dict[str, str | int | float | bool | None] = Field(default_factory=dict)


class RunManifest(BaseModel):
  run_id: str
  created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
  input: RunInput
  stages: list[StageRecord] = Field(default_factory=list)