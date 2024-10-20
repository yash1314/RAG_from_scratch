# RAG-P: A Retrieval-Augmented Generation Chatbot

This project implements a Retrieval-Augmented Generation (RAG) chatbot built from scratch using Python. The chatbot allows users to upload documents, transform them into embeddings, perform similarity searches, and generate context-driven responses using an LLM (Language Model). The application follows a modular structure and uses APIs and models from Hugging Face for document embeddings and answer generation.

## Features
- **Document Upload and Management**: Upload and delete user documents.
- **Document Embedding**: The documents are split into chunks and converted into embeddings using Hugging Face's Sentence Transformer model.
- **Query Similarity Search**: User queries are embedded and compared with document embeddings using cosine similarity to retrieve the most relevant context.
- **LLM-Generated Answers**: The most relevant context is used by an LLM via Hugging Face Gradio API to generate final answers.
- **Logging and Exception Handling**: Thorough logging and error handling implemented throughout the application.
- **Modular Code Design**: The project is structured for clarity, separation of concerns, and ease of maintenance.

## Project Structure
```
RAG_P/
├── .streamlit/              # Streamlit configuration
├── .venv/                   # Virtual environment
├── extras/                  # Extra files (if any)
├── logs/                    # Logs for debugging
├── resources/               # Static resources such as CSS files
│   ├── animation.py         # Animation utilities
├── src/                     # Main source code
│   ├── data_components/      # Components handling data operations
│   │   ├── data_ingestion.py         # File upload, processing, and ingestion
│   │   ├── data_similarity_search.py # Similarity search using cosine distance
│   │   ├── data_transform.py         # Data transformation logic (chunking, embedding)
│   ├── model_components/     # Components handling models
│   │   ├── models.py                 # Embedding and model handling logic
│   ├── pipelines/            # Pipelines and orchestration
│   │   ├── exception.py              # Exception handling
│   │   ├── logger.py                 # Logging setup and management
├── app.py                   # Main Streamlit app entry point
├── design.css               # Custom CSS for Streamlit design
├── requirements.txt         # List of dependencies
├── utils.py                 # Utility functions for the app
```

## Pipeline Overview

1. **File Upload**: 
   - Users upload a document (text, PDF, etc.).
   - The file is processed and converted into a Pandas DataFrame where each row corresponds to a chunk of text from the document.
   - This data is then saved as a CSV file and embedded using a pre-trained Sentence Transformer from Hugging Face.

2. **Document Embedding**:
   - The document chunks are embedded using the Hugging Face embedding model. Each chunk's embedding is stored in the CSV alongside its index for reference during similarity search.

3. **Query Embedding and Search**:
   - The user submits a query, which is also embedded using the same embedding model.
   - A cosine similarity search is performed between the query embedding and document embeddings, retrieving the most 02 similar chunks.

4. **Answer Generation**:
   - The retrieved chunk is sent as context to a 7B parameter LLM using Hugging Face Gradio API, which generates a final answer for the user.

## How to Run Locally

### Prerequisites
- Python 3.8 or higher
- Install dependencies using the provided `requirements.txt`

### Steps

1. **Clone the repository**:
   ```bash
   git clone <repo_url>
   cd RAG_P
2. **Create a virtual environment:**
  python3 -m venv .venv
source .venv/bin/activate  # For Linux/MacOS
 .venv\Scripts\activate    # For Windows

3. **Install the required packages:**
   pip install -r requirements.txt

4. **Run the application:**
   streamlit run app.py

5. Interact with the chatbot: Upload documents, submit queries, and receive context-driven responses via the app's UI.

## Technologies and Tools Used
- Python: Core language for developing the application.
- Streamlit: Used for creating the front-end interface.
- Hugging Face Sentence Transformer: For embedding document chunks and user queries.
- Hugging Face Gradio API: For generating responses using a 7B parameter LLM model.
- Pandas: For handling document data transformation.
- Cosine Similarity: For matching the user query to the most relevant document context.
- Logging and Exception Handling: Ensures smooth operation and debugging.

## Future Enhancements
- Add support for more file formats.
- Improve the performance of similarity search for large documents.
- Optimize the chunking and embedding process for better accuracy.

Author: Yash Keshari
