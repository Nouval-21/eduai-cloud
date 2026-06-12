from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Material
from app.services import storage_service

router = APIRouter(prefix="/api/materials", tags=["Materials"])

@router.get("/")
async def get_materials(db: Session = Depends(get_db)):
    materials = db.query(Material).order_by(Material.created_at.desc()).all()
    return {
        "materials": [
            {
                "id": m.id,
                "filename": m.title,
                "url": m.file_url,
                "key": m.file_key,
                "subject": m.subject,
            }
            for m in materials
        ]
    }

@router.post("/upload")
async def upload_material(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        file_content = await file.read()
        result = storage_service.upload_file(
            file_content,
            file.filename,
            file.content_type
        )
        material = Material(
            title=file.filename,
            subject="Umum",
            description=None,
            file_key=result["key"],
            file_url=result["url"],
        )
        db.add(material)
        db.commit()
        db.refresh(material)
        return {"id": material.id, "filename": file.filename, "url": result["url"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{material_id}")
async def delete_material(material_id: int, db: Session = Depends(get_db)):
    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    try:
        storage_service.delete_file(material.file_key)
    except Exception:
        pass
    db.delete(material)
    db.commit()
    return {"message": "Material deleted successfully"}