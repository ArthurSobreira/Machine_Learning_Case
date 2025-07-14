from typing import BinaryIO
import pdfplumber


def extract_text(file_stream: BinaryIO) -> str:
  """
  Extracts structured text from PDF, handling page rotation and tables.
  
  Args:
      file_stream: Binary stream of the PDF file
      
  Returns:
      Extracted text content with formatted tables
  """

  content = []
  file_stream.seek(0)
  
  with pdfplumber.open(file_stream) as pdf:
    for page_number, page in enumerate(pdf.pages, start=1):
      rotation = page.rotation
      if rotation:
        page = page.crop(page.bbox).rotate(-rotation)
      
      page_content = [f"\n--- Page {page_number} ---\n"]
      
      text_content = page.extract_text()
      if text_content:
        page_content.append(text_content + "\n")
      
      tables = page.find_tables()
      if tables:
        page_content.append("\n[Tables Found]\n")
          
      for table_idx, table in enumerate(tables, start=1):
        table_data = table.extract()
        
        table_rows = []
        for row in table_data:
          formatted_row = [
            str(cell).replace('\n', ' ') if cell else ""
            for cell in row
          ]
          table_rows.append("| " + " | ".join(formatted_row) + " |")

        table_str = "\n".join(table_rows)
        page_content.append(f"\nTABLE {table_idx}:\n{table_str}\n")
      
      content.append("\n".join(page_content))

  return "\n".join(content).strip()