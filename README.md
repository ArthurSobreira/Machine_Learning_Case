
# Ask Question API

> *This is a simple movie catalog API built with **Django** and **Django REST Framework (DRF)**.*
> *It allows you to list and access movie details. The API is ready to be consumed by a frontend application*
> *(**Next.js** in this project's case) and has the following endpoints:*

## 1. Documents Upload Endpoint

- **Method:** `POST`
- **Endpoint:** `/documents`
- **Description:** Uploads one or more documents to be indexed:

  - `files`: One or more PDF files.

**Example response:**

```json
    {
        "message": "Documents processed successfully",
        "documents_indexed": 2,
        "total_chunks": 128
    } 
```

<br>

## 2. Ask Question Endpoint

- **Method:** `POST`
- **Endpoint:** `/question`
- **Description:** : Aks a question that will be answered using a LLM model:

     - `question`: The question should be placed at the 'question' field in the request body.

**Example response:**

```json
{
    "answer": "what is the pwer consumption of the motor",
    "nome": "The Godfather",
    "imagem_url": 
}
```
