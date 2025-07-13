
# Ask Question API

> *This is a document processing API built with FastAPI. It allows users to upload PDF documents,* 
> *process their contents, and ask questions about the uploaded documents. The API is designed to* 
> *integrate with a frontend application or other systems and provides the following endpoints:*

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
    "answer": "The motor's power consumption is 2.3 kW.",
    "references": [
      "the motor xxx has requires 2.3kw to operate at a 60hz line frequency"
    ]
}
```
