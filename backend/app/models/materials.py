from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Material
from app.services.storage_service import upload_file, get_presigned_url, delete_file

router = APIRouter(prefix="/api/materials", tags=["Materials"])

@router.post("/upload")
async def upload_material(
    title: str = Form(...),
    subject: str = Form(...),
    description: str = Form(""),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    allowed_types = ["application/pdf", "image/jpeg", "image/png", "image/jpg"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Format file tidak didukung. Gunakan PDF, JPG, atau PNG.")
    content = await file.read()
    result = upload_file(content, file.filename, file.content_type)
    material = Material(
        title=title, subject=subject, description=description,
        file_key=result["key"], file_url=result["url"]
    )
    db.add(material)
    db.commit()
    db.refresh(material)
    return {"id": material.id, "title": title, "subject": subject,
            "url": result["url"], "message": "File berhasil diupload!"}

@router.get("/")
def list_materials(subject: str = None, db: Session = Depends(get_db)):
    query = db.query(Material)
    if subject:
        query = query.filter(Material.subject == subject)
    materials = query.order_by(Material.created_at.desc()).all()
    result = []
    for m in materials:
        url = get_presigned_url(m.file_key) if m.file_key else m.file_url
        result.append({"id": m.id, "title": m.title, "subject": m.subject,
                       "description": m.description, "url": url})
    return result

@router.delete("/{material_id}")
def delete_material(material_id: int, db: Session = Depends(get_db)):
    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Materi tidak ditemukan")
    if material.file_key:
        delete_file(material.file_key)
    db.delete(material)
    db.commit()
    return {"message": "Materi berhasil dihapus"}