# 📚 LLM-RAG App Documentation

Welcome to the **LLM-RAG App** repository! This project leverages **ZenML** for building robust pipelines and integrates **OpenAI's GPT-4o** for intelligent document analysis. The app is designed to allow users to upload PDF files, perform document retrieval, and ask dynamic questions—including generating summaries.

---

## 🚀 **Table of Contents**
1. [Features](#features)  
2. [Installation Guide](#installation-guide)  
3. [Project Structure](#project-structure)  
4. [Pipeline Overview](#pipeline-overview)  
5. [Components Breakdown](#components-breakdown)  
6. [Usage Instructions](#usage-instructions)  
7. [Logging and Monitoring](#logging-and-monitoring)  
8. [Troubleshooting](#troubleshooting)  
9. [Contributing](#contributing)  
10. [License](#license)

---

## ✨ **Features**
- Upload and analyze PDF documents.
- Dynamic Q&A based on document content.
- Summarization of documents using GPT-4o.
- Built on a robust ZenML pipeline.
- Detailed logging for monitoring and debugging.

---

## ⚙️ **Installation Guide**

### 1️⃣ **Clone the Repository:**
```bash
git clone https://github.com/drbn68/llm-rag-app.git
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
poetry run uvicorn app.main:app --reload --log-level debug
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
│   └── logs/            # Directory for log files (e.g., app.log)
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

## 📥 **Usage Instructions**

1. **Access API Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
2. **Upload a PDF:** Use the `/ask` endpoint to upload a PDF.
3. **Ask a Question:** Enter a question like:
   - "Summarize this document."
   - "What are the key findings of the study?"
   - "Which species migrates earlier?"
4. **Receive Response:** The app processes the document and returns the answer.

---

## 📊 **Logging and Monitoring**

The app includes robust logging features to track API requests, pipeline executions, and debugging information.

### 🔍 **Log Details:**
- All logs are saved in `app/logs/app.log`.
- Logs include request details, pipeline run statuses, and errors.

### 🗒️ **Log Configuration:**
The logging configuration can be found in `main.py`:
```python
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app/logs/app.log", mode='w'),
        logging.StreamHandler()
    ]
)
```

To run with debug logging:
```bash
poetry run uvicorn app.main:app --reload --log-level debug
```

---

## 🛠️ **Troubleshooting**

- **Common Errors:**
  - `Invalid 'max_tokens'`: Adjust token calculation logic.
  - `Server Error: ArtifactVersionResponse`: Ensure ZenML artifact loading is correct.
- **Debugging Tips:**
  - Check `app/logs/app.log` for detailed logs.
  - Use `traceback` for error tracking.
  - Verify `.env` file for correct API key.

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
4. Push and create a pull request:
   ```bash
   git push origin feature-branch
   ```

---

## 📜 **License**
This project is licensed under the **MIT License**.

> Built with FastAPI, ZenML, and OpenAI GPT-4o.

