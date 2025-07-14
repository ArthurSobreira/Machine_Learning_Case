from typing import List
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def select_top_k_chunks(
    question_embedding: list, 
    embeddings: List[list], 
    chunks: List[str], 
    k: int = 5
  ) -> List[str]:
  """
  Select the top-k most relevant text chunks based on cosine similarity.
  
  Args:
    question_embedding (list): The embedding vector of the user's question.
    embeddings (List[list]): A list of embedding vectors for the text chunks.
    chunks (List[str]): A list of text chunks corresponding to the embeddings.
    k (int): The number of top chunks to select.

  Returns:
    List[str]: A list of most (k) relevant text chunks.
  """

  # Calculate cosine similarities between the question embedding and all chunk embeddings
  similarities = cosine_similarity([question_embedding], embeddings)[0]
  
  # Sort the similarities and get the indices of the top k chunks
  top_indices = np.argsort(similarities)[-k:][::-1]

  return [chunks[i] for i in top_indices]
