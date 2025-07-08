from PyPDF2 import PdfReader

def extract_text_from_pdf(file_stream) -> str:
  # """Recebe um stream de PDF e retorna o texto extraído"""
  reader = PdfReader(file_stream)
  text = ""

  for page in reader.pages:
    text += page.extract_text() or ""

  return text.strip()
