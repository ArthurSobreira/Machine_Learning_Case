from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from typing import List, Optional
# from src.core.qa.qa_session import QASession 


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
    # qa = QASession()
    # answer, references = qa.answer_question(question)

    answer, references = "Sample answer", ["Reference 1", "Reference 2"]

    return {
      "answer": answer,
      "references": references
    }

  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error answering question: {str(e)}")
