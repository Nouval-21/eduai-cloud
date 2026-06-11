from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services import storage_service
import uuid

router = APIRouter()

@router.get("/")
async def get_materials():
    return {"materials": []}

@router.post("/upload")
async def upload_material(file: UploadFile = File(...)):
    try:
        file_content = await file.read()
        result = storage_service.upload_file(
            file_content,
            file.filename,
            file.content_type
        )
        return {"id": str(uuid.uuid4()), "filename": file.filename, "url": result["url"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{material_id}")
async def delete_material(material_id: str):
    try:
        storage_service.delete_file(material_id)
        return {"message": "Material deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))