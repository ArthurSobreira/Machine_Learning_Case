from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from typing import BinaryIO, List, Dict, Any
from datetime import datetime
import pdfplumber
import os
import json
import pickle
import re


class PDFHandler:
  def __init__(self, file_stream: BinaryIO, file_name: str):
    self._file_stream = file_stream
    self._filename = file_name
    self._text = ""
    self._chunks: List[str] = []
    self._embeddings = []
    self._metadata: Dict[str, Any] = {}
    self._embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

  @property
  def chunks(self) -> List[str]:
    """
    Returns the list of text chunks to external access.
    """
    return self._chunks

  def process(self) -> None:
    """
    Execute the complete PDF processing pipeline.
    """

    self._extract_text()
    self._clean_text()
    self._chunk_text()
    self._generate_embeddings()
    self._save_to_disk()

  def _extract_text(self) -> None:
    """
    Extracts structured text from the PDF, including formatted tables.
    """
    
    content = ""
    self._file_stream.seek(0)
    
    with pdfplumber.open(self._file_stream) as pdf:
      for page_number, page in enumerate(pdf.pages, start=1):
        content += f"\n--- Page {page_number} ---\n"
        
        text_content = page.extract_text()
        if text_content:
          content += text_content + "\n\n"
        
        tables = page.find_tables()
        for table_idx, table in enumerate(tables, start=1):
          table_data = table.extract()

          table_str = ""
          for row in table_data:
            clean_row = [str(cell).replace('\n', ' ') if cell else "" for cell in row]
            table_str += "| " + " | ".join(clean_row) + " |\n"
            
          content += f"\n[TABLE {table_idx}]\n{table_str}\n"
    
    self._text = content.strip()

  def _clean_text(self) -> None:
    """
    Cleans the extracted text by removing unnecessary characters and formatting.
    """
    
    self._text = re.sub(r'\s+', ' ', self._text)
    self._text = re.sub(r'--- Page \d+ ---', '\n\\g<0>\n', self._text)

  def _chunk_text(self, chunk_size: int = 1000, chunk_overlap: int = 100) -> None:
    """
    Split the text into semantic chunks.
    
    Args:
      chunk_size (int): The maximum size of each chunk.
      chunk_overlap (int): The number of overlapping characters between chunks.
    """
    
    splitter = RecursiveCharacterTextSplitter(
      chunk_size=chunk_size,
      chunk_overlap=chunk_overlap,
      separators=["\n\n", "\n", ". ", "! ", "? ", "; ", ", ", " ", ""]
    )
    
    self._chunks = splitter.split_text(self._text)

  def _generate_embeddings(self) -> None:
    """
    Generates vector embeddings for each chunk of text.
    """
    
    if not self.chunks:
        raise ValueError("Chunks não disponíveis. Execute chunk_text() primeiro.")
    
    self._embeddings = self._embedding_model.encode(
        self.chunks, 
        show_progress_bar=True,
        convert_to_tensor=False
    ).tolist()

  def _save_to_disk(self, base_path: str = "data") -> None:
    """
    Save the processed PDF data to disk.
    
    Args:
      base_path (str): The base directory where the data will be saved.
    """

    doc_dir = os.path.join(base_path, self._filename.replace(".pdf", ""))
    os.makedirs(doc_dir, exist_ok=True)

    self._metadata = {
      "filename": self._filename,
      "pages": self._text.count("--- Page"),
      "total_chunks": len(self.chunks),
      "created_at": datetime.now().isoformat(),
    }

    if not os.access(doc_dir, os.W_OK):
      raise PermissionError(f"No permission to write to directory: {doc_dir}")

    # Save the complete text to a file
    with open(os.path.join(doc_dir, "text.txt"), "w", encoding="utf-8") as f:
      f.write(self._text)

    # Save the chunks to a JSON file
    with open(os.path.join(doc_dir, "chunks.json"), "w", encoding="utf-8") as f:
      json.dump(self.chunks, f, indent=2, ensure_ascii=False)

    # Save the embeddings to a pickle file
    with open(os.path.join(doc_dir, "embeddings.pkl"), "wb") as f:
      pickle.dump(self._embeddings, f)

    # Save metadata to a JSON file
    with open(os.path.join(doc_dir, "metadata.json"), "w", encoding="utf-8") as f:
      json.dump(self._metadata, f, indent=2)
