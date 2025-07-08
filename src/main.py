from core.pdf_reader import extract_text_from_pdf


def main():
  # pdf_path = "/Users/arthursobreira/repos/case_tractian/case_files/LB5001.pdf"
  pdf_path = "./LB5001.pdf" # caminho dentro do container
  
  try:
    with open(pdf_path, "rb") as pdf_file:
      extracted_text = extract_text_from_pdf(pdf_file)
      print("conteudo: ")
      print(extracted_text)
  except FileNotFoundError:
    print(f"erro: {pdf_path}")
  except Exception as e:
    print(f"erro: {e}")

if __name__ == "__main__":
  main()
