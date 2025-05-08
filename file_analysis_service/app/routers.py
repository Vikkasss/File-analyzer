import hashlib
import uuid
import httpx
from http.client import HTTPException
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import AnalysisResult as AnalysisResultModel

router = APIRouter()

@router.post("/analyze")
async def analyze_file(file_id: str, db: Session = Depends(get_db)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://api-gateway:8000/files/{file_id}/content")
            if response.status_code != 200:
                raise HTTPException(404, "File not found")

            content = response.json()["content"]
            file_hash = hashlib.sha256(content.encode()).hexdigest()

        result = AnalysisResultModel(
            id=str(uuid.uuid4()),
            content=content,
            hash=file_hash,
        )
        db.add(result)
        db.commit()
        db.refresh(result)

        return {"result_id": result.id,
                "content": result.content,
                "hash": result.hash
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.post("/compare")
async def compare_files(file_id1: str, file_id2: str):
    async with httpx.AsyncClient() as client:
        response1 = await client.get(f"http://api-gateway:8000/files/{file_id1}")
        response2 = await client.get(f"http://api-gateway:8000/files/{file_id2}")

        if response1.status_code != 200 or response2.status_code != 200:
            raise HTTPException(404, "Files not found")

        hash1 = response1.json()["hash"]
        hash2 = response2.json()["hash"]

        return {"hash_match": hash1 == hash2}

