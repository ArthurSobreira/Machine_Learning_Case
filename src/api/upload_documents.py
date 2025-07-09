from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import io

from src.core.pdf_reader import extract_text_from_pdf 

router = APIRouter()

@router.post("/documents")
async def upload_documents(files: List[UploadFile] = File(...)):
  results = []

  for file in files:
    if file.content_type != "application/pdf":
      raise HTTPException(status_code=400, detail=f"'{file.filename}' não é um PDF válido.")

    try:
      file_bytes = await file.read()
      content = extract_text_from_pdf(io.BytesIO(file_bytes))
      results.append({
        "filename": file.filename,
        "size_kb": round(len(file_bytes) / 1024, 2),
        "content_snippet": content[:300]  # tirar depois
      })
    except Exception as e:
      raise HTTPException(status_code=500, detail=f"Erro ao processar '{file.filename}': {str(e)}")

  return {
    "status": "ok",
    "documents_processed": len(results),
    "documents": results
  }
