from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import create_student, get_student
from ..schemas import StudentCreate, StudentRead

router = APIRouter(prefix="/api/students", tags=["students"])

@router.post("/", response_model=StudentRead)
def create(s: StudentCreate, db: Session = Depends(get_db)):
    return create_student(db, s)

@router.get("/{id}", response_model=StudentRead)
def read(id: int, db: Session = Depends(get_db)):
    student = get_student(db, id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student