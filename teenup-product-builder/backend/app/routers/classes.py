from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import create_class, get_classes_by_day, register_to_class
from ..schemas import ClassCreate, ClassRead, ClassRegistrationCreate

router = APIRouter(prefix="/api/classes", tags=["classes"])

@router.post("/", response_model=ClassRead)
def create(c: ClassCreate, db: Session = Depends(get_db)):
    return create_class(db, c)

@router.get("/", response_model=list[ClassRead])
def list_classes(day: str = None, db: Session = Depends(get_db)):
    """GET /api/classes?day=Monday"""
    return get_classes_by_day(db, day)

@router.post("/{class_id}/register", response_model=dict)
def register(class_id: int, reg: ClassRegistrationCreate, db: Session = Depends(get_db)):
    """POST /api/classes/{class_id}/register - body: {"student_id": 1}"""
    try:
        registration = register_to_class(db, class_id, reg.student_id)
        return {"message": "Đăng ký thành công", "registration_id": registration.id}
    except HTTPException as e:
        raise e