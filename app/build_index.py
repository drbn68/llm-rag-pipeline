from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
import fitz  # PyMuPDF

# ✅ Function to extract text from a PDF
def extract_text_from_pdf(file_path):
    pdf = fitz.open(file_path)
    text = ""
    for page in pdf:
        text += page.get_text()
    return text

# ✅ Function to split text into smaller chunks for embedding
def split_text(text):
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return [Document(page_content=chunk) for chunk in splitter.split_text(text)]

# ✅ Main function to build FAISS index
def build_faiss_index(file_path):
    text = extract_text_from_pdf(file_path)
    documents = split_text(text)

    model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    faiss_index = FAISS.from_documents(documents, model)

    faiss_index.save_local("faiss_index")
    print("✅ FAISS index created and saved successfully!")

# ✅ Replace with your PDF file path
build_faiss_index("path_to_your_document.pdf")
