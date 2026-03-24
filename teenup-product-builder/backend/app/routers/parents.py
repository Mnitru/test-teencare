from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import create_parent, get_parent
from ..schemas import ParentCreate, ParentRead

router = APIRouter(prefix="/api/parents", tags=["parents"])

@router.post("/", response_model=ParentRead)
def create(p: ParentCreate, db: Session = Depends(get_db)):
    return create_parent(db, p)

@router.get("/{id}", response_model=ParentRead)
def read(id: int, db: Session = Depends(get_db)):
    parent = get_parent(db, id)
    if not parent: raise HTTPException(404, "Not found")
    return parent