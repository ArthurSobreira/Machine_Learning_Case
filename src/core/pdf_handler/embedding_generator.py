from typing import List
from sentence_transformers import SentenceTransformer


def generate_embeddings(chunks: List[str], model: SentenceTransformer) -> list:
  """
  Generates vector embeddings for each chunk of text.
  
  Args:
    chunks (List[str]): The list of text chunks to be embedded.
    model (SentenceTransformer): The pre-trained model used for generating embeddings.
    
  Returns:
    list: A list of embeddings.
  """

  if not chunks:
    raise ValueError("No chunks available")
  
  return model.encode(
    chunks, 
    show_progress_bar=True,
    convert_to_tensor=False
  ).tolist()
