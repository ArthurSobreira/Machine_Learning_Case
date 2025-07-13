from typing import BinaryIO
import pdfplumber


def extract_text(file_stream: BinaryIO) -> str:
  content = ""
  file_stream.seek(0)
  
  with pdfplumber.open(file_stream) as pdf:
    for page_number, page in enumerate(pdf.pages, start=1):
      content += f"\n--- Page {page_number} ---\n"
      
      text_content = page.extract_text()
      if text_content:
        content += text_content + "\n\n"
      
      tables = page.find_tables()
      for table_idx, table in enumerate(tables, start=1):
        table_data = table.extract()
        table_str = "\n".join(
          "| " + " | ".join(str(cell).replace('\n', ' ') if cell else "" for cell in row) + " |"
          for row in table_data
        )
        content += f"\n[TABLE {table_idx}]\n{table_str}\n"

  return content.strip()
