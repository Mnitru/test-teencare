from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId

from app.database import get_db
from app.schemas import ParentCreate, ParentRead

router = APIRouter(prefix="/api/parents", tags=["parents"])

@router.post("/", response_model=ParentRead)
def create(p: ParentCreate, db=Depends(get_db)):
    data = p.dict()
    result = db.parents.insert_one(data)
    data["id"] = str(result.inserted_id)
    return data

@router.get("/{id}", response_model=ParentRead)
def read(id: str, db=Depends(get_db)):
    parent = db.parents.find_one({"_id": ObjectId(id)})
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")

    parent["id"] = str(parent["_id"])
    del parent["_id"]
    return parent