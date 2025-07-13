from typing import List, Dict, Any
import os
import json
import pickle

def save_to_disk(
    base_path: str,
    filename: str,
    text: str,
    chunks: List[str],
    embeddings: list,
    metadata: Dict[str, Any]
) -> None:

  doc_dir = os.path.join(base_path, filename.replace(".pdf", ""))
  os.makedirs(doc_dir, exist_ok=True)

  if not os.access(doc_dir, os.W_OK):
    raise PermissionError(f"No write permission for: {doc_dir}")

  # Text save
  with open(os.path.join(doc_dir, "text.txt"), "w", encoding="utf-8") as f:
    f.write(text)

  # Chunks save
  with open(os.path.join(doc_dir, "chunks.json"), "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2, ensure_ascii=False)

  # Embeddings save
  with open(os.path.join(doc_dir, "embeddings.pkl"), "wb") as f:
    pickle.dump(embeddings, f)

  # Metadata save
  with open(os.path.join(doc_dir, "metadata.json"), "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)
