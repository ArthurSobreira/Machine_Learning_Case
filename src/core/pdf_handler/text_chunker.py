from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter


def chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
  """
  Split the text into semantic chunks.

  Args:
    chunk_size (int): The maximum size of each chunk.
    chunk_overlap (int): The number of overlapping characters between chunks.

  Returns:
    List[str]: A list of text chunks.
  """

  splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
    separators=["\n\n", "\n", ". ", "! ", "? ", "; ", ", ", " ", ""]
  )
  return splitter.split_text(text)
