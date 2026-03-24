from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from datetime import date

from app.database import get_db
from app.schemas import SubscriptionCreate, SubscriptionRead

router = APIRouter(prefix="/api/subscriptions", tags=["subscriptions"])


@router.post("/", response_model=SubscriptionRead)
def create(s: SubscriptionCreate, db=Depends(get_db)):
    data = s.dict()
    data.setdefault("used_sessions", 0)

    result = db.subscriptions.insert_one(data)

    data["id"] = str(result.inserted_id)
    return data


@router.patch("/{id}/use", response_model=SubscriptionRead)
def use(id: str, db=Depends(get_db)):
    sub = db.subscriptions.find_one({"_id": ObjectId(id)})
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")

    if sub["used_sessions"] >= sub["total_sessions"]:
        raise HTTPException(status_code=400, detail="Đã hết số buổi học")

    db.subscriptions.update_one(
        {"_id": ObjectId(id)},
        {"$inc": {"used_sessions": 1}}
    )

    sub = db.subscriptions.find_one({"_id": ObjectId(id)})
    sub["id"] = str(sub["_id"])
    del sub["_id"]
    return sub


@router.get("/{id}", response_model=SubscriptionRead)
def read(id: str, db=Depends(get_db)):
    sub = db.subscriptions.find_one({"_id": ObjectId(id)})
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")

    sub["id"] = str(sub["_id"])
    del sub["_id"]
    return sub