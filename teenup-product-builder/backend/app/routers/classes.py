from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId

from app.database import get_db
from app.schemas import ClassCreate, ClassRead, ClassRegistrationCreate

router = APIRouter(prefix="/api/classes", tags=["classes"])

@router.post("/", response_model=ClassRead)
def create(c: ClassCreate, db=Depends(get_db)):
    data = c.dict()
    result = db.classes.insert_one(data)
    data["id"] = str(result.inserted_id)
    return data

@router.get("/", response_model=list[ClassRead])
def list_classes(day: str | None = None, db=Depends(get_db)):
    query = {}
    if day:
        query["day_of_week"] = day

    classes = []
    for cls in db.classes.find(query):
        cls["id"] = str(cls["_id"])
        del cls["_id"]
        classes.append(cls)

    return classes

@router.post("/{class_id}/register")
def register(class_id: str, reg: ClassRegistrationCreate, db=Depends(get_db)):
    cls = db.classes.find_one({"_id": ObjectId(class_id)})
    if not cls:
        raise HTTPException(404, "Class not found")

    # check sĩ số
    count = db.class_registrations.count_documents({"class_id": class_id})
    if count >= cls["max_students"]:
        raise HTTPException(400, "Lớp đã đầy")

    registration = {
        "class_id": class_id,
        "student_id": reg.student_id
    }
    result = db.class_registrations.insert_one(registration)

    return {
        "message": "Đăng ký thành công",
        "registration_id": str(result.inserted_id)
    }