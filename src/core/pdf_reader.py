# from PyPDF2 import PdfReader
# from tabula import read_pdf
# import pandas as pd
import pdfplumber


def extract_text_from_pdf(file_stream) -> str:
  content = ""

  file_stream.seek(0)
  with pdfplumber.open(file_stream) as pdf:
    for page_number, page in enumerate(pdf.pages, start=1):
      content += f"\n--- Página {page_number} ---\n"
      elements = []

      words = page.extract_words()
      if words:
        lines = {}
        for word in words:
          y0 = round(word['top'], 1)
          lines.setdefault(y0, []).append(word['text'])

        for y0, words_at_y in lines.items():
          text_line = ' '.join(words_at_y)
          elements.append({
            "type": "text",
            "y0": y0,
            "text": text_line
          })

      tables = page.find_tables()
      for i, table in enumerate(tables, start=1):
        table_y = table.bbox[1]
        extracted = table.extract()

        table_str = ""
        for row in extracted:
          cleaned_row = [
            str(cell).replace('\n', ' ') if cell is not None else ""
            for cell in row
          ]
          table_str += "| " + " | ".join(cleaned_row) + " |\n"

        elements.append({
          "type": "table",
          "y0": table_y,
          "text": f"[Tabela {i}]\n{table_str}"
        })

      elements.sort(key=lambda x: x["y0"])

      for el in elements:
        content += el["text"] + "\n"

  return content.strip()



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
