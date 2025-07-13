from typing import List
from sentence_transformers import SentenceTransformer

def generate_embeddings(chunks: List[str], model: SentenceTransformer) -> list:
  if not chunks:
    raise ValueError("No chunks available")
  
  return model.encode(
    chunks, 
    show_progress_bar=True,
    convert_to_tensor=False
  ).tolist()
