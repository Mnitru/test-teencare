from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import create_subscription, use_session, get_subscription
from ..schemas import SubscriptionCreate, SubscriptionRead

router = APIRouter(prefix="/api/subscriptions", tags=["subscriptions"])

@router.post("/", response_model=SubscriptionRead)
def create(s: SubscriptionCreate, db: Session = Depends(get_db)):
    return create_subscription(db, s)

@router.patch("/{id}/use", response_model=SubscriptionRead)
def use(id: int, db: Session = Depends(get_db)):
    """PATCH /api/subscriptions/{id}/use - đánh dấu dùng 1 buổi"""
    sub = use_session(db, id)
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return sub

@router.get("/{id}", response_model=SubscriptionRead)
def read(id: int, db: Session = Depends(get_db)):
    sub = get_subscription(db, id)
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return sub