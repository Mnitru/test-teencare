from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import delete_registration
from ..models import ClassRegistration, Class, Student

router = APIRouter(prefix="/api/registrations", tags=["registrations"])

# GET danh sách tất cả đăng ký (để hiển thị trên UI)
@router.get("/")
def list_registrations(db: Session = Depends(get_db)):
    regs = db.query(ClassRegistration).all()
    result = []
    for r in regs:
        cls = db.query(Class).filter(Class.id == r.class_id).first()
        stu = db.query(Student).filter(Student.id == r.student_id).first()
        result.append({
            "id": r.id,
            "student_name": stu.name if stu else "Unknown",
            "class_name": cls.name if cls else "Unknown",
            "class_id": r.class_id,
            "student_id": r.student_id
        })
    return result

# DELETE hủy đăng ký
@router.delete("/{id}")
def cancel(id: int, db: Session = Depends(get_db)):
    try:
        return delete_registration(db, id)
    except HTTPException as e:
        raise e