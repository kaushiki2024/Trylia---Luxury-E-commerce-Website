from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.models import User
from app.schemas.schemas import TryOnSessionCreate, TryOnSessionRead
from app.services.session_service import create_tryon_session, list_user_sessions


router = APIRouter(prefix="/sessions", tags=["sessions"]) 


@router.post("/", response_model=TryOnSessionRead)
def create_session(payload: TryOnSessionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    session = create_tryon_session(
        db,
        user_id=current_user.user_id,
        photo_id=payload.photo_id,
        outfit_id=payload.outfit_id,
        result_url=payload.result_url,
    )
    return session


@router.get("/", response_model=list[TryOnSessionRead])
def list_sessions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_user_sessions(db, current_user.user_id)

