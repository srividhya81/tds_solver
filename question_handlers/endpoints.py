from fastapi import APIRouter, UploadFile, File
from fastapi.responses import HTMLResponse
from typing import Union

router = APIRouter()

@router.post("/api")
async def handle_request(
    question: Union[str, UploadFile, HTMLResponse]
):
    if isinstance(question, str):
        return {"response": f"Received text question: {question}"}
    elif isinstance(question, UploadFile):
        content = await question.read()
        return {"response": f"Received file: {question.filename}", "content": content.decode("utf-8")}
    elif isinstance(question, HTMLResponse):
        return {"response": "Received HTML content"}
    else:
        return {"error": "Unsupported input type"}