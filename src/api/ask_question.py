from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
# from src.core.qa.qa_session import QASession 

qa_router = APIRouter()

class AskRequest(BaseModel):
  question: str
  document_name: str
  model: Optional[str] = "gpt-3.5"

class AskResponse(BaseModel):
  answer: str
  references: List[str]

@qa_router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
  try:
    # qa = QASession(document_name=request.document_name, model_name=request.model)
    # answer, references = qa.answer_question(request.question)

    return AskResponse(answer=answer, references=references)

  except FileNotFoundError:
    raise HTTPException(status_code=404, detail="Documento não encontrado.")
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Erro ao processar pergunta: {str(e)}")
