from sentence_transformers import SentenceTransformer
from .loader import load_from_disk
from .chunk_selector import select_top_k_chunks
from .llm_caller import call_model
from typing import List


class QAHandler:
  def __init__(self):
    self._chunks: List[str] = []
    self._embeddings: List[List[float]] = []
    self._question_embedding: List[float] = []
    self._model_name: str = "gpt-3.5"
    self._embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

  def answer_question(self, question: str):
    """
    Executes the complete question-answering pipeline.

    Args:
      question (str): The user's question.
      model (str): The name of the model to use for answering the question.
    """
    if not question or question.strip() == "":
      raise ValueError("Question cannot be empty.")

    self._generate_question_embedding(question)
    self._load_from_disk()

    if not self._chunks or not self._embeddings:
      raise RuntimeError("No chunks or embeddings loaded. Call load_from_disk() first.")

    top_chunks = select_top_k_chunks(self._question_embedding, self._embeddings, self._chunks)
    context = "\n".join(top_chunks)

    answer = call_model(question=question, context=context)
    
    return answer, top_chunks

  def _generate_question_embedding(self, question: str) -> None:
    """
    Generate an embedding for the user's question.
    
    Args:
      question (str): The user's question to be embedded.
    """
    model = self._embedding_model
    self._question_embedding = model.encode(
      question,
      show_progress_bar=True,
      convert_to_tensor=False
    ).tolist()

  def _load_from_disk(self) -> None:
    """Load processed chunks and embeddings from disk."""
    self._chunks, self._embeddings = load_from_disk()
