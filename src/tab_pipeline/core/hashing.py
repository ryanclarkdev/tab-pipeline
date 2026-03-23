from hashlib import sha256
from pathlib import Path


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
  digest = sha256()

  with path.open("rb") as file_obj:
    while chunk := file_obj.read(chunk_size):
      digest.update(chunk)

  return digest.hexdigest()