from typing import List
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def select_top_k_chunks(
    question_embedding: list, 
    embeddings: List[list], 
    chunks: List[str], 
    k: int = 5
  ) -> List[str]:

  # Calculate cosine similarities between the question embedding and all chunk embeddings
  similarities = cosine_similarity([question_embedding], embeddings)[0]
  
  # Sort the similarities and get the indices of the top k chunks
  top_indices = np.argsort(similarities)[-k:][::-1]

  return [chunks[i] for i in top_indices]
