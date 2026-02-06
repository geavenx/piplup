from pathlib import Path

import uvicorn
from fastapi import FastAPI, UploadFile, HTTPException

app = FastAPI()


def cli():
    uvicorn.run("app.main:app", host="100.69.243.42", port=6969, reload=True)


IMAGES_DIR = Path.home() / "Images"


@app.post("/upload")
async def upload_image(file: UploadFile):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    file_path = IMAGES_DIR / file.filename
    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    return {"filename": file.filename, "path": str(file_path)}
