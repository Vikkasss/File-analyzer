import hashlib
import uuid
from http.client import HTTPException
from fastapi import APIRouter, UploadFile, File, Depends
from pathlib import Path
from sqlalchemy.orm import Session
from .database import get_db
from .models import File as FileModel

router = APIRouter()

STORAGE_PATH = Path('storage')
STORAGE_PATH.mkdir(exist_ok=True)

@router.post('/files')
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        file_id = str(uuid.uuid4())
        content = await file.read()
        file_hash = hashlib.sha256(content).hexdigest()

        file_location = STORAGE_PATH / f"{file_id}.txt"
        with open(file_location, "wb") as f:
            f.write(content)

        db_file = FileModel(
            id = file_id,
            name = file.filename,
            hash = file_hash,
            location = str(file_location),
        )

        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        return {"file_id": file_id,
                "filename": file.filename,
                "hash": file_hash,
                "location": str(file_location)
                }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading file {str(e)}"
        )
    finally:
        await file.close()


@router.get("/files/{file_id}")
def get_file(file_id: str, db: Session = Depends(get_db)):
    file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file:
        raise HTTPException(404, "File not found")
    return file

@router.get("/files/{file_id}/content")
def get_file_content(file_id: str, db: Session = Depends(get_db)):
    file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file:
        raise HTTPException(404, "File not found")
    with open(file.location, "r") as f:
        content = f.read()

    return {"content": content}