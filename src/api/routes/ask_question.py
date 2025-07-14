from fastapi import APIRouter, Body, HTTPException
from src.core.qa_handler import QAHandler


question_router = APIRouter()

@question_router.post("/question")
async def ask_question(question: str = Body(..., embed=True)):
  """
  Endpoint for asking a question based on uploaded PDF(s).

  Args:
    question (str): User's question.

  Returns:
    dict: Answer and references.
  """

  try:
    qa_handler = QAHandler()
    answer, references = qa_handler.answer_question(question)

    return {
      "answer": answer,
      "references": references
    }

  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error answering question: {str(e)}")
