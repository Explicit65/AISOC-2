from typing import List, Literal, Any
from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import JSONResponse
from werkzeug.utils import secure_filename
from main import *
from helpers import file_checks
from helpers import upload_file
import os, tempfile

app = FastAPI()

@app.get('/healthz')
async def health():
    return {
        "application": "Simple LLM API",
        "message": "running succesfully"
    }


@app.post('/upload')
async def process(
    files: List[UploadFile] = None,
    urls: List[str] = None
):
    
    # query = await request.json()

            documents = SimpleDirectoryReader(temp_dir).load_data()
            embeddings = VectorStoreIndex.from_documents(documents)

    


if __name__ == "__main__":
    import uvicorn
    print("Starting LLM API")
    uvicorn.run(app, host="0.0.0.0", reload=True)