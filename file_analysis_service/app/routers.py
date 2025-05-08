import hashlib
import uuid
import httpx
from http.client import HTTPException
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .models import AnalysisResult as AnalysisResultModel
from .analyser import analyze_text

router = APIRouter()

@router.post("/analyze")
async def analyze_file(file_id: str, db: Session = Depends(get_db)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://api-gateway:8000/files/{file_id}/content")
            if response.status_code != 200:
                raise HTTPException(404, "File not found")

            content = response.json()["content"]
            st = analyze_text(content)
            if content is None:
                raise HTTPException(status_code=500, detail="Content missing in response")

        result = AnalysisResultModel(
            id=str(uuid.uuid4()),
            content=content,
            word_count=st.word_count,
            char_count=st.char_count,
            paragraph_count=st.paragraph_count
        )
        db.add(result)
        db.commit()
        db.refresh(result)

        return {"analysis_id": result.id,
                "content": result.content,
                "word_count": result.word_count,
                "char_count": result.char_count,
                "paragraph_count": result.paragraph_count
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/analyze/{analysis_id}")
async def analyze_file(analysis_id: str, db: Session = Depends(get_db)):
    content = db.query(AnalysisResultModel).filter(AnalysisResultModel.id == analysis_id).first()
    if not content:
        raise HTTPException(404, "Content not found")
    return {
        "analysis_id": content.id,
        "word_count": content.word_count,
        "char_count": content.char_count,
        "paragraph_count": content.paragraph_count
    }


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

