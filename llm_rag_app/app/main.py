from fastapi import FastAPI, UploadFile
from retriever import load_retriever
from generator import generate_answer

app = FastAPI()
retriever = load_retriever()

@app.post("/ask")
async def ask_question(file: UploadFile, question: str):
    content = await file.read()
    docs = content.decode().split("\n")
    relevant_docs = retriever.similarity_search(question, docs)
    context = " ".join([doc.page_content for doc in relevant_docs])
    answer = generate_answer(context, question)
    return {"answer": answer}
