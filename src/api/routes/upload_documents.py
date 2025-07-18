from fastapi import APIRouter, UploadFile, File, HTTPException
from src.core.pdf_handler import PDFHandler
from typing import List
from io import BytesIO


documents_router = APIRouter()

@documents_router.post("/documents")
async def upload_documents(files: List[UploadFile] = File(...)):
  """
  Endpoin to uploading and processing PDF documents.
  
  Args:
    files (List[UploadFile]): List of files sent in the request.
  
  Returns:
    dict: A dictionary containing the number of documents indexed and total chunks processed.
  """

  if not files:
    raise HTTPException(status_code=400, detail="No files were provided.")

  total_chunks = 0
  documents_indexed = 0

  for file in files:
    if file.content_type != "application/pdf":
      raise HTTPException(status_code=400, detail=f"'{file.filename}' is not a valid PDF file.")

    try:
      file_bytes = await file.read()
      processor = PDFHandler(BytesIO(file_bytes), file.filename)
      processor.process()

      total_chunks += len(processor.chunks)
      documents_indexed += 1
    except Exception as e:
      raise HTTPException(status_code=500, detail=f"Error processing '{file.filename}': {str(e)}")

  return {
    "message": "Documents processed successfully",
    "documents_indexed": documents_indexed,
    "total_chunks": total_chunks
  }
