from fastapi import FastAPI, UploadFile, Form, File, HTTPException
from app.rag_pipeline import rag_pipeline
from dotenv import load_dotenv
from zenml.client import Client
from zenml.materializers import BuiltInMaterializer
import os
import traceback

# ✅ Load environment variables
load_dotenv()

app = FastAPI()

@app.post("/ask")
async def ask_question(
    question: str = Form(...),
    file: UploadFile = File(...)
):
    file_path = f"temp_{file.filename}"

    try:
        # ✅ Save uploaded PDF temporarily
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # ✅ Run the RAG pipeline
        pipeline_run = rag_pipeline(file_path, question)
        client = Client()

        # ✅ Get the latest run of the RAG pipeline
        last_run = client.get_pipeline("rag_pipeline").last_successful_run

        # ✅ Retrieve the output from the generation step
        generation_step = last_run.steps["generation_step"]
        output_artifacts = generation_step.outputs["output"]  # List of ArtifactVersionResponse

        # ✅ Use BuiltInMaterializer to load artifact content
        def load_artifact_content(artifact):
            materializer = BuiltInMaterializer(uri=artifact.uri)
            return materializer.load(data_type=str)  # ✅ Specify data_type as str

        # ✅ Handle both single and multiple outputs
        if isinstance(output_artifacts, list):
            answer = " ".join([load_artifact_content(artifact) for artifact in output_artifacts])
        else:
            answer = load_artifact_content(output_artifacts)

        return {"answer": answer}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")

    finally:
        # ✅ Clean up temporary file
        if os.path.exists(file_path):
            os.remove(file_path)
