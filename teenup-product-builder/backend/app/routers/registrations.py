from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId

from app.database import get_db

router = APIRouter(prefix="/api/registrations", tags=["registrations"])

@router.get("/")
def list_registrations(db=Depends(get_db)):
    results = []

    for reg in db.class_registrations.find():
        cls = db.classes.find_one({"_id": ObjectId(reg["class_id"])})
        stu = db.students.find_one({"_id": ObjectId(reg["student_id"])})

        results.append({
            "id": str(reg["_id"]),
            "class_id": reg["class_id"],
            "student_id": reg["student_id"],
            "class_name": cls["name"] if cls else "Unknown",
            "student_name": stu["name"] if stu else "Unknown"
        })

    return results

@router.delete("/{id}")
def cancel(id: str, db=Depends(get_db)):
    reg = db.class_registrations.find_one({"_id": ObjectId(id)})
    if not reg:
        raise HTTPException(404, "Registration not found")

    db.class_registrations.delete_one({"_id": ObjectId(id)})
    return {"message": "Đã hủy đăng ký"}