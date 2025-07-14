# [Challenge] Machine Learning Engineering - LLM

> *This project was developed as a technical challenge and implements a system that allows users to upload PDF documents and later ask questions about their contents.*

## Project Overview

This system was designed to perform **document ingestion**, **chunk-based semantic search**, and **retrieval-augmented generation (RAG)** using a Large Language Model (LLM). The workflow is divided into two main phases:

- **Document Upload:** The user uploads one or more PDF documents via the `/documents` endpoint. These documents are processed to extract their full content, including tables, and then split into meaningful chunks. Each chunk is transformed into an embedding vector and stored locally.
- **Question Answering:** The user submits a question via the `/question` endpoint. The system generates an embedding of the question, compares it with all stored chunks, retrieves the most relevant ones, and sends them as context to the selected LLM to generate a concise and accurate answer.

For more information about the API Specifications, you can access it [README](src/api/README.md).

---

## Running the Project

### Requirements

- [Docker](https://www.docker.com/) and [Make](https://www.gnu.org/software/make/) installed;
- An **OpenAI API Key** (to be added in a `.env` file, at the root of the repository), if you want, you can use this one:

```bash
  OPENAI_API_KEY=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
```

### Project Setup

* Make sure you clone the repository with the following command:

  ```bash
  $> git clone git@github.com:ArthurSobreira/Machine_Learning_Case.git
  ```

* Build the Docker Image

  ```bash
  $> make build
  ```

* Run the Project

  ```bash
  $> make run
  ```

The server will be started and the API will be accessible at `http://127.0.0.1:8000/`.

* If you have any questions about the available commands, use:

  ```bash
  $> make help
  ```
