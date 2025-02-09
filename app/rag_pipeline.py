from zenml.pipelines import pipeline
from zenml.steps import step
from app.retriever import build_retriever
from app.generator import generate_answer

# 🔍 Step 1: Build the Retriever
@step
def retriever_step(file_path: str, question: str) -> list:
    """
    Retrieves relevant documents based on the question.
    """
    retriever = build_retriever(file_path)
    documents = retriever.get_relevant_documents(question)  # ✅ Dynamically retrieve based on the question
    return [doc.page_content for doc in documents]  # ✅ Convert to list of strings (JSON serializable)

# ✏️ Step 2: Combine Retrieved Documents
@step
def combine_context_step(context_list: list) -> str:
    """
    Combines the retrieved document content into a single string.
    """
    combined_context = " ".join(context_list)  # ✅ Merge all texts into one
    return combined_context

# ✨ Step 3: Generate Answer Using LLM
@step
def generation_step(context: str, question: str) -> str:
    """
    Generates an answer based on the combined context and the user's question.
    """
    answer = generate_answer(context, question)
    return answer

# 🚀 Final RAG Pipeline Orchestration
@pipeline
def rag_pipeline(file_path: str, question: str):
    """
    Executes the RAG pipeline:
    1️⃣ Retrieves documents based on the question
    2️⃣ Combines them into a unified context
    3️⃣ Generates an answer
    """
    context_list = retriever_step(file_path, question)  # ✅ Dynamic retrieval
    combined_context = combine_context_step(context_list)  # ✅ Improved readability
    answer = generation_step(combined_context, question)
    return answer
