from fastapi import FastAPI, File, UploadFile, HTTPException
from utils import preprocess


app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

@app.post("/upload")
async def process_pdf_type_one(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are accepted.")
    # Procesa tu archivo PDF aquí
    return {"message": f"PDF Type One Processed: {file.filename}"}

@app.post("/upload/type-two")
async def process_pdf_type_two(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are accepted.")
    # Procesa tu archivo PDF aquí
    return {"message": f"PDF Type Two Processed: {file.filename}"}
