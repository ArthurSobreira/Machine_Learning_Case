from dotenv import load_dotenv
import openai
import os

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are an expert technical assistant. Follow these rules strictly:
1. Answer ONLY based on the provided context
2. Always respond in English, unless the user specifies otherwise
3. Be concise and technical
4. Format answers clearly using markdown when appropriate
5. Never invent information

Context:
{context}
"""

def call_model(
    question: str,
    context: str,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.1,
    max_tokens: int = 1024
) -> str:
  """
  Sends a question and context to LLM and returns the generated answer.

  Args:
    question (str): User's question
    context (str): Context to help answer the question

  Returns:
    str: Generated answer from the LLM
  """

  if not client.api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set")

  formatted_prompt = SYSTEM_PROMPT.format(context=context)

  try:
    response = client.chat.completions.create(
      model=model,
      messages=[
        {"role": "system", "content": formatted_prompt},
        {"role": "user", "content": question}
      ],
      temperature=temperature,
      max_tokens=max_tokens,
      top_p=0.9,
      frequency_penalty=0.1,
      presence_penalty=0.1,
    )

    return response.choices[0].message.content.strip()

  except Exception as e:
    raise RuntimeError(f"LLM API error: {str(e)}") from e
