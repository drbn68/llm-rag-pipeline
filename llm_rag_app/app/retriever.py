from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

def load_retriever():
    model = HuggingFaceEmbeddings()
    retriever = FAISS.load_local("faiss_index", model)
    return retriever
