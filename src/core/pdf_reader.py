# from PyPDF2 import PdfReader
# from tabula import read_pdf
# import pandas as pd
import pdfplumber


def extract_text_from_pdf(file_stream) -> str:
  text = ""
  try:
    file_stream.seek(0) 
    with pdfplumber.open(file_stream) as pdf:
      for page_number, page in enumerate(pdf.pages, start=1):
        text += f"\n--- Página {page_number} ---\n"
        
        page_text = page.extract_text()
        if page_text:
          text += page_text + "\n"
        
        tables = page.find_tables()
        if tables:
          text += "\n--- Tabelas ---\n"
          for i, table in enumerate(tables, start=1):
            df = table.extract()
            
            table_str = ""
            for row in df:
              cleaned_row = [
                  str(cell).replace('\n', ' ') if cell is not None else ""
                  for cell in row
              ]
              table_str += " | ".join(cleaned_row) + "\n"
            
            text += f"\n----- Tabela {i}: -----\n"
            text += table_str + "\n"

  except Exception as e:
    print(f"Erro ao ler o PDF: {e}")
  
  return text.strip()

# def extract_text_from_pdf(file_stream) -> str:
#   """Recebe um stream de PDF e retorna o conteúdo extraído"""
#   text = ""

#   try:
#     reader = PdfReader(file_stream)
#     for page_number, page in enumerate(reader.pages, start=1):
#       text += f"\n--- Página {page_number} ---\n"
#       text += page.extract_text() or ""

#       tables = read_pdf(file_stream, pages=page_number, multiple_tables=True, pandas_options={"header": None})
#       if tables:
#         text += "\n--- Tabelas ---\n"
#         for i, table in enumerate(tables, start=1):
#           text += f"\n----- Tabela {i}: ----- \n"
#           text += table.to_string(index=False, header=False) + "\n"

#   except Exception as e:
#     print(f"Erro ao ler o PDF: {e}")
    
#   # for page in reader.pages:
#   #   text += page.extract_text() or ""

#   # Modificar a leitura para usar tabula-py

#   return text.strip()
