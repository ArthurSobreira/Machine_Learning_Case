import os
import json
import pickle
from typing import BinaryIO, List
from datetime import datetime

import pdfplumber
from sentence_transformers import SentenceTransformer

class PDFHandler:
  def __init__(self, file_stream: BinaryIO, file_name: str):
    self.file_stream = file_stream
    self.filename = file_name
    self.text = ""
    self.chunks: List[str] = []
    self.embeddings = []
    self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    # def extract_text(self) -> str:
    #     """
    #     Extract text from the PDF file.
    #     """
    #     try:
    #         from PyPDF2 import PdfReader
    #         reader = PdfReader(self.pdf_path)
    #         text = ''
    #         for page in reader.pages:
    #             text += page.extract_text() or ''
    #         return text
    #     except Exception as e:
    #         raise RuntimeError(f"Failed to extract text from PDF: {e}")
    
  def save_to_disk(self, base_path: str = "data") -> None:
    """
    Save the processed PDF data to disk.
    
    Args:
      base_path (str): The base directory where the data will be saved.
    """

    doc_dir = os.path.join(base_path, self.filename.replace(".pdf", ""))
    os.makedirs(doc_dir, exist_ok=True)

    # 1. Salva o texto completo
    with open(os.path.join(doc_dir, "text.txt"), "w", encoding="utf-8") as f:
      f.write(self.text)

    # 2. Salva os chunks como JSON
    with open(os.path.join(doc_dir, "chunks.json"), "w", encoding="utf-8") as f:
      json.dump(self.chunks, f, indent=2, ensure_ascii=False)

    # 3. Salva os embeddings como pickle
    with open(os.path.join(doc_dir, "embeddings.pkl"), "wb") as f:
      pickle.dump(self.embeddings, f)

    # 4. Salva metadados do processamento
    metadata = {
      "filename": self.filename,
      "pages": self.text.count("--- Página "),
      "total_chunks": len(self.chunks),
      "created_at": datetime.now().isoformat(),
    }

    with open(os.path.join(doc_dir, "metadata.json"), "w", encoding="utf-8") as f:
      json.dump(metadata, f, indent=2)
        
    