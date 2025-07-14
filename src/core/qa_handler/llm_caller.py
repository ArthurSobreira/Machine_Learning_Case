import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def call_model(question: str, context: str) -> str:
  """
  Sends a question and context to LLM and returns the generated answer.

  Args:
    question (str): User's question
    context (str): Context to help answer the question

  Returns:
    str: Generated answer from the LLM
  """

  try:
    system_prompt = (
      "Você é um assistente técnico. Use o contexto abaixo para responder à pergunta. "
      "Se a resposta não estiver presente no contexto, diga que não sabe com base nos dados disponíveis.\n\n"
      f"Context:\n{context}"
    )

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
      ],
      temperature=0.2,
      max_tokens=512,
    )

    return response.choices[0].message["content"].strip()

  except Exception as e:
    raise RuntimeError(f"Error calling LLM: {str(e)}")
