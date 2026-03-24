from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId

from app.database import get_db
from app.schemas import StudentCreate, StudentRead

router = APIRouter(prefix="/api/students", tags=["students"])

@router.post("/", response_model=StudentRead)
def create(s: StudentCreate, db=Depends(get_db)):
    data = s.dict()
    result = db.students.insert_one(data)
    data["id"] = str(result.inserted_id)
    return data

@router.get("/{id}", response_model=StudentRead)
def read(id: str, db=Depends(get_db)):
    student = db.students.find_one({"_id": ObjectId(id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student["id"] = str(student["_id"])
    del student["_id"]
    return student