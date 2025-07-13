from .text_extractor import extract_text
from .text_cleaner import clean_text
from .text_chunker import chunk_text
from .embedding_generator import generate_embeddings
from .disk_saver import save_to_disk
from sentence_transformers import SentenceTransformer
from typing import BinaryIO, List, Dict, Any
from datetime import datetime


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
    """Returns the list of text chunks to external access."""
    return self._chunks

  def process(self) -> None:
    """Execute the complete PDF processing pipeline."""
    self._extract_text()
    self._clean_text()
    self._chunk_text()
    self._generate_embeddings()
    self._save_to_disk()

  def _extract_text(self) -> None:
    """Extracts structured text from the PDF, including formatted tables."""
    self._text = extract_text(self._file_stream)

  def _clean_text(self) -> None:
    """Cleans the extracted text by removing unnecessary characters and formatting."""
    self._text = clean_text(self._text)

  def _chunk_text(self, chunk_size: int = 1000, chunk_overlap: int = 100) -> None:
    """
    Split the text into semantic chunks.
    
    Args:
      chunk_size (int): The maximum size of each chunk.
      chunk_overlap (int): The number of overlapping characters between chunks.
    """
    self._chunks = chunk_text(self._text, chunk_size, chunk_overlap)

  def _generate_embeddings(self) -> None:
    """Generates vector embeddings for each chunk of text."""
    self._embeddings = generate_embeddings(self._chunks, self._embedding_model)

  def _save_to_disk(self, base_path: str = "data") -> None:
    """
    Save the processed PDF data to disk.
    
    Args:
      base_path (str): The base directory where the data will be saved.
    """
    self._metadata = {
      "filename": self._filename,
      "pages": self._text.count("--- Page"),
      "total_chunks": len(self.chunks),
      "created_at": datetime.now().isoformat(),
    }
    save_to_disk(
      base_path=base_path,
      filename=self._filename,
      text=self._text,
      chunks=self._chunks,
      embeddings=self._embeddings,
      metadata=self._metadata
    )
