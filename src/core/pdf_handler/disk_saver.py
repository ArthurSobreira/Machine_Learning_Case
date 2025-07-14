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
  """
  Save the processed PDF data to disk.
  
  Args:
    base_path (str): The base directory where the data will be saved.
    filename (str): The name of the PDF file being processed.
    text (str): The extracted text from the PDF.
    chunks (List[str]): The list of text chunks.
    embeddings (list): The list of embeddings for the text chunks.
    metadata (Dict[str, Any]): Metadata about the PDF file and processing.
  """

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
