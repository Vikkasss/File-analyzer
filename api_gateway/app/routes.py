from http.client import responses
from fastapi import APIRouter, UploadFile, File, HTTPException
import httpx

router = APIRouter()


async def call_service(url: str):
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    except httpx.ConnectError:
        raise HTTPException(503, detail="Сервис временно недоступен")
    except httpx.TimeoutException:
        raise HTTPException(504, detail="Таймаут соединения")
    except httpx.HTTPStatusError as e:
        raise HTTPException(e.response.status_code, detail=e.response.text)

@router.post("/files")
async def upload_file(file: UploadFile = File(...)):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://file-storing:8002/files",
            files={"file": (file.filename, await file.read())}
        )
        return response.json()

@router.get("/files/{file_id}")
async def get_file(file_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://file-storing:8002/files/{file_id}")
        return response.json()


@router.get("/files/{file_id}/content")
async def get_file_content(file_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://file-storing:8002/files/{file_id}/content")
        return response.json()


@router.post("/analyze")
async def analyze_file(file_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"http://file-analysis:8001/analyze?file_id={file_id}")
        return response.json()

@router.get("/analyze/{analyze_id}")
async def get_analyze_file(analyze_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://file-analysis:8001/analyze/{analyze_id}")
        return response.json()

@router.post("/compare")
async def compare_file(file_id1: str, file_id2: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://file-analysis:8001/compare",
            params={"file_id1": file_id1, "file_id2": file_id2}
        )
        return response.json()

