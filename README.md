# 📚 LLM-RAG App Documentation

Welcome to the **LLM-RAG App** repository! This project leverages **ZenML** for building robust pipelines and integrates **OpenAI's GPT-4o** for intelligent document analysis. The app is designed to allow users to upload PDF files, perform document retrieval, and ask dynamic questions—including generating summaries.

---

## 🚀 **Table of Contents**
1. [Features](#features)  
2. [Installation Guide](#installation-guide)  
3. [Project Structure](#project-structure)  
4. [Pipeline Overview](#pipeline-overview)  
5. [Components Breakdown](#components-breakdown)  
6. [Workflow Explanation](#workflow-explanation)  
7. [Usage Instructions](#usage-instructions)  
8. [Troubleshooting](#troubleshooting)  
9. [Contributing](#contributing)  
10. [License](#license)

---

## ✨ **Features**
- Upload and analyze PDF documents.
- Dynamic Q&A based on document content.
- Summarization of documents using GPT-4o.
- Built on a robust ZenML pipeline.

---

## ⚙️ **Installation Guide**

### 1️⃣ **Clone the Repository:**
```bash
git clone https://github.com/yourusername/llm-rag-app.git
cd llm-rag-app
```

### 2️⃣ **Set Up the Environment:**
Ensure you have **Python 3.11+** installed.
```bash
pip install poetry
poetry install
poetry shell
```

### 3️⃣ **Configure Environment Variables:**
Create a `.env` file in the root directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 4️⃣ **Run the App:**
```bash
poetry run uvicorn app.main:app --reload
```
Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🗂️ **Project Structure**
```
llm-rag-app/
├── app/
│   ├── main.py          # FastAPI app entry point
│   ├── retriever.py     # Handles document retrieval with FAISS
│   ├── generator.py     # Generates answers using OpenAI GPT-4o
│   ├── rag_pipeline.py  # ZenML pipeline orchestration
├── .env                 # API keys
├── README.md            # Project documentation
├── poetry.lock          # Poetry dependencies lock file
└── pyproject.toml       # Project dependencies and configurations
```

---

## 🧪 **Pipeline Overview**

The application follows the **RAG (Retrieval-Augmented Generation)** pattern, orchestrated by **ZenML**.

### 🔄 **Workflow:**
1. **File Upload:** User uploads a PDF file via the FastAPI endpoint.
2. **Retriever Step:** Extracts and splits the text using FAISS.
3. **Context Combination:** Merges relevant document chunks.
4. **Answer Generation:** Uses OpenAI GPT-4o for generating responses.
5. **Response Delivery:** Returns the response to the user.

---

## 🧩 **Components Breakdown**

### 1️⃣ **Retriever (`retriever.py`):**
- Extracts text from PDFs.
- Splits text into manageable chunks.
- Builds FAISS index for efficient document retrieval.

### 2️⃣ **Generator (`generator.py`):**
- Uses OpenAI's GPT-4o.
- Dynamically adjusts token limits.
- Handles continuation of responses to avoid truncation.

### 3️⃣ **ZenML Pipeline (`rag_pipeline.py`):**
- **Retriever Step:** Loads document chunks.
- **Context Step:** Combines text chunks into a unified context.
- **Generation Step:** Passes the context and question to GPT-4o.

### 4️⃣ **FastAPI (`main.py`):**
- Provides API endpoints for file upload and question submission.
- Manages error handling and response formatting.

---

## 🔗 **Workflow Explanation**

### 📥 **1. User Uploads a PDF and Submits a Question**
- **Endpoint Triggered:** `POST /ask` in `main.py`
- **Inputs:**
  - **PDF file**: Uploaded by the user.
  - **Question**: Submitted through the form.

### 🚀 **2. FastAPI Handles the Request (`main.py`)**
- **Temporary File Creation:** 
  - The uploaded PDF is saved temporarily on the server.
- **Pipeline Trigger:**
  - A unique run ID is generated using `uuid`.
  - The `rag_pipeline` function is called with the PDF file path and the user's question as arguments.

### 🔄 **3. RAG Pipeline Starts (`rag_pipeline.py`)**
The pipeline orchestrates three main steps:

1. **Retriever Step (`retriever.py`):**
   - **PDF Reading:** Extracts the text content from the uploaded PDF.
   - **Text Splitting:** Breaks the text into smaller chunks for efficient processing.
   - **Embedding Generation:** Converts text chunks into numerical vector representations (embeddings).
   - **FAISS Indexing:** Creates an index using FAISS for fast retrieval of relevant chunks based on similarity to the question.

2. **Context Combination Step:**
   - **Query Processing:** Takes the user's question and searches the FAISS index for the most relevant text chunks.
   - **Context Assembly:** Combines these chunks into a single context string to be used by the language model.

3. **Generation Step (`generator.py`):**
   - **Prompt Creation:** Constructs a prompt using the retrieved context and the user's question.
   - **Answer Generation:** Sends the prompt to OpenAI’s GPT-4 model to generate a comprehensive, context-aware answer.

### 📤 **4. Retrieving the Pipeline Output (`main.py`)**
- **Pipeline Monitoring:**
  - The app waits for the pipeline to complete and fetches the output of the `generation_step`.
- **Artifact Loading:**
  - The generated answer is retrieved from the output artifact using `BuiltInMaterializer`.

### 🗑️ **5. Response & Cleanup**
- **Response:** 
  - The generated answer is returned to the user as a JSON response.
- **File Cleanup:** 
  - The temporary PDF file is deleted from the server to save space.

### 📝 **Summary of the Flow**

1. **`main.py`**: Handles the request, saves the PDF, and triggers the pipeline.
2. **`rag_pipeline.py`**: Orchestrates the pipeline steps.
3. **`retriever.py`**: Extracts, splits, and indexes PDF content with FAISS.
4. **`generator.py`**: Generates an answer using the retrieved content and GPT-4.
5. **`main.py`**: Retrieves the final output, sends it back to the user, and cleans up.

---

## 📥 **Usage Instructions**

1. **Access API Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
2. **Upload a PDF:** Use the `/ask` endpoint to upload a PDF.
3. **Ask a Question:** Enter a question like:
   - "Summarize this document."
   - "What are the key findings of the study?"
   - "Which species migrates earlier?"
4. **Receive Response:** The app processes the document and returns the answer.

---

## 🛠️ **Troubleshooting**
- **Common Errors:**
  - `Invalid 'max_tokens'`: Adjust token calculation logic.
  - `Server Error: ArtifactVersionResponse`: Ensure ZenML artifact loading is correct.
- **Debugging Tips:**
  - Use `traceback` for detailed error logs.
  - Check `.env` file for API key issues.

---

## 🤝 **Contributing**

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Make changes and commit:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push and create a pull request.

---

## 📜 **License**
This project is licensed under the **MIT License**.

> Built with ❤️ using FastAPI, ZenML, and OpenAI GPT-4o.

