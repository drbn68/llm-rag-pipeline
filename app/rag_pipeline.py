from zenml.pipelines import pipeline
from zenml.steps import step
from app.retriever import build_retriever
from app.generator import generate_answer
import tiktoken  # For accurate token counting

# ✅ Token counter for managing limits
def count_tokens(text: str, model: str = "gpt-4o-mini") -> int:
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))

# 🔍 Step 1: Build the Retriever (Data Ingestion)
@step
def retriever_step(file_path: str, question: str) -> list:
    retriever = build_retriever(file_path)
    documents = retriever.get_relevant_documents(question)

    # ✅ Limit to top 2 documents (minimize tokens)
    top_documents = documents[:2]
    return [doc.page_content for doc in top_documents]

# ✏️ Step 2: Combine Retrieved Chunks (Token-Aware)
@step
def combine_context_step(context_list: list) -> str:
    combined_context = "\n".join(context_list)

    # ✅ Token limit enforcement (keep < 150,000 tokens)
    max_tokens = 150000
    while count_tokens(combined_context) > max_tokens:
        context_list.pop()  # Remove the last chunk
        combined_context = "\n".join(context_list)

    return combined_context

# ✨ Step 3: Generate Answer Using LLM (Token Control)
@step
def generation_step(context: str, question: str) -> str:
    # ✅ Limit output to 1,000 tokens
    max_output_tokens = 1000
    answer = generate_answer(context, question, max_tokens=max_output_tokens)
    return answer

# 🚀 Final Optimized RAG Pipeline
@pipeline
def rag_pipeline(file_path: str, question: str):
    context_list = retriever_step(file_path, question)
    combined_context = combine_context_step(context_list)
    answer = generation_step(combined_context, question)
    return answer
