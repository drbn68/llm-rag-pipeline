from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
import fitz  # PyMuPDF

# ✅ Extract text from PDF
def extract_text_from_pdf(file_path):
    try:
        pdf = fitz.open(file_path)
        text = ""
        for page in pdf:
            text += page.get_text()
        return text
    except Exception as e:
        raise ValueError(f"Error extracting text from {file_path}: {str(e)}")

# ✅ Split text into manageable chunks
def split_text(text):
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)  # Adjusted for better context
    return [Document(page_content=chunk) for chunk in splitter.split_text(text)]

# ✅ Build FAISS retriever
def build_retriever(file_path):
    # 1️⃣ Extract text from the PDF
    text = extract_text_from_pdf(file_path)
    
    # 2️⃣ Split the text into chunks for retrieval
    documents = split_text(text)
    
    # 3️⃣ Embed the text using a Sentence Transformer model
    model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # 4️⃣ Create a FAISS index from the embedded documents
    faiss_index = FAISS.from_documents(documents, model)
    
    # 5️⃣ Return the retriever interface for RAG pipeline
    return faiss_index.as_retriever()  # ✅ Ensures compatibility with the RAG pipeline
