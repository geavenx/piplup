import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Header, UploadFile, HTTPException

from app.utils import get_clipboard, require_auth, set_clipboard

load_dotenv()
app = FastAPI()


IMAGES_DIR = Path.home() / "Images"

HOST = os.environ.get("PIPLUP_HOST", "0.0.0.0")
PORT = os.environ.get("PIPLUP_PORT", "6969")

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

class ContentClipboard(BaseModel):
    text: str

@app.post("/clipboard")
async def push_clipboard(
    content: ContentClipboard,
    authorization: Optional[str] = Header(default=None),
):

    require_auth(authorization)
    if not content.text:
        raise HTTPException(400, "Empty clipboard")

    if len(content.text) > 1_000_000:
        raise HTTPException(status_code=413, detail="Too large")
    try:
        set_clipboard(content.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return "OK"


@app.get("/clipboard")
async def pull_clipboard(authorization: Optional[str] = Header(default=None)):
    require_auth(authorization)
    try:
        return get_clipboard()
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


def cli():
    uvicorn.run("app.main:app", host=HOST, port=int(PORT), reload=False)
