from PyPDF2 import PdfReader
import pdfplumber

def extract_text_from_pdf(file_stream) -> str:
  """Recebe um stream de PDF e retorna o texto extraído"""
  # reader = PdfReader(file_stream)
  text = ""

  # for page in reader.pages:
  #   text += page.extract_text() or ""

  with pdfplumber.open(file_stream) as pdf:
    for page in pdf.pages:
      text += page.extract_text() + "\n"

  return text.strip()
