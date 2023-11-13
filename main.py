from typing import Annotated
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
import os
from models import Wish
from wish_processor import process_wish

app = FastAPI()

# Directory where uploaded files will be saved
UPLOAD_DIRECTORY = "data"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# @app.post("/files/")
# async def create_files(
    # files: Annotated[list[bytes], File(description="Multiple files as bytes")],
# ):
    # for index, file in enumerate(files):
        # file_path = os.path.join(UPLOAD_DIRECTORY, f"file_{index}")
        # with open(file_path, "wb") as f:
            # f.write(file)
    # return {"message": "Files saved successfully"}


@app.post("/uploaddocuments/")
async def upload_documents(
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    for file in files:
        if not file.filename.lower().endswith('.pdf'):
            # Raise an exception for non-PDF files
            raise HTTPException(status_code=400, detail=f"File '{file.filename}' is not a PDF.")

        contents = await file.read()
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_path, "wb") as f:
            f.write(contents)
    return {"message": "PDF files uploaded successfully"}

@app.get("/documents/")
async def list_documents():
    return {"documents": os.listdir(UPLOAD_DIRECTORY)}

@app.post("/wish/")
async def make_a_wish_to_genie(wish: Wish):
    grant = process_wish(wish)
    return grant

@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
