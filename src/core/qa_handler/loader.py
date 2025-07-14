import os
import json
import pickle
from typing import List, Tuple

def load_from_disk(base_path: str = "data") -> Tuple[List[str], List[List[float]]]:
  """
  Load all chunks and embeddings from the specified base path.
  
  Args:
    base_path (str): The base directory where the data is stored.
  
  Returns:
    Tuple[List[str], List[List[float]]]:
      - List of all text chunks (List[str])
      - List of embeddings (List[List[float]])
  """

  all_chunks: List[str] = []
  all_embeddings: List[List[float]] = []

  if not os.path.exists(base_path):
    raise FileNotFoundError(f"Base path '{base_path}' does not exist.")

  for dir_name in os.listdir(base_path):
    dir_path = os.path.join(base_path, dir_name)

    if not os.path.isdir(dir_path):
      continue

    chunks_path = os.path.join(dir_path, "chunks.json")
    embeddings_path = os.path.join(dir_path, "embeddings.pkl")

    if not os.path.exists(chunks_path) or not os.path.exists(embeddings_path):
      continue

    try:
      with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

      with open(embeddings_path, "rb") as f:
        embeddings = pickle.load(f)

      if len(chunks) != len(embeddings):
        continue

      all_chunks.extend(chunks)
      all_embeddings.extend(embeddings)

    except Exception as e:
      print(f"Error loading data from {dir_name}: {e}")
      continue

  if not all_chunks or not all_embeddings:
    raise RuntimeError("No valid chunks or embeddings found in the base path.")

  return all_chunks, all_embeddings