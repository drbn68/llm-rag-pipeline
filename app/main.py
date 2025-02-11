import logging
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from app.rag_pipeline import rag_pipeline
from zenml.client import Client
from zenml.materializers import BuiltInMaterializer
import os
import uuid

# ✅ Logging Configuration
log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# ✅ File Handler
file_handler = logging.FileHandler("app.log", mode='w', encoding='utf-8')
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.DEBUG)

# ✅ Console Handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.DEBUG)

# ✅ Logger Setup
logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

# ✅ Clear Existing Handlers
if logger.hasHandlers():
    logger.handlers.clear()

# ✅ Add Handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.debug("FastAPI server has started...")

# ✅ FastAPI App
app = FastAPI()

@app.get("/test-log")
async def test_log():
    logger.info("Test log entry works!")
    return {"message": "Log test completed!"}

@app.post("/ask")
async def ask_question(
    question: str = Form(...),
    file: UploadFile = File(...)
):
    file_path = f"temp_{file.filename}"

    try:
        logger.info(f"Received question: '{question}' with file: '{file.filename}'")

        # ✅ Save uploaded PDF temporarily
        with open(file_path, "wb") as f:
            f.write(await file.read())
        logger.info(f"Saved file to {file_path}")

        client = Client()

        # ✅ Generate a unique run name
        unique_run_name = f"rag_run_{uuid.uuid4()}"
        logger.info(f"Starting pipeline run with ID: {unique_run_name}")

        # ✅ Trigger the pipeline
        run = rag_pipeline(file_path=file_path, question=question)
        logger.info("Pipeline execution initiated.")

        # ✅ Wait for the pipeline to complete
        last_run = client.get_pipeline("rag_pipeline").last_successful_run
        logger.info(f"Pipeline execution completed. Run ID: {last_run.id}")

        # ✅ Retrieve the output from the generation step
        generation_step = last_run.steps.get("generation_step")
        output_artifacts = generation_step.outputs.get("output")
        logger.info("Retrieved output artifacts from generation step.")

        # ✅ Use BuiltInMaterializer to load artifact content
        def load_artifact_content(artifact):
            logger.info(f"Loading artifact from URI: {artifact.uri}")
            materializer = BuiltInMaterializer(uri=artifact.uri)
            content = materializer.load(data_type=str)
            logger.debug(f"Retrieved content sample: {content[:300]}")  # Log first 300 characters
            return content

        # ✅ Handle both single and multiple outputs correctly
        if isinstance(output_artifacts, list):
            answers = [load_artifact_content(artifact) for artifact in output_artifacts if hasattr(artifact, 'uri')]
            answer = " ".join(answers) if answers else "No valid output found."
        elif hasattr(output_artifacts, 'uri'):
            answer = load_artifact_content(output_artifacts)
        else:
            answer = "No valid output found."

        logger.info(f"Generated answer: {answer[:100]}...")  # Log first 100 characters

        return {"answer": answer}

    except Exception as e:
        logger.error("An error occurred:", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")

    finally:
        # ✅ Clean up temporary file
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Deleted temporary file: {file_path}")
