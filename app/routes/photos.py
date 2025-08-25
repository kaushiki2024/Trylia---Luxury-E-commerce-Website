from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.models import User
from app.schemas.schemas import UserPhotoCreate, UserPhotoRead
from app.services.photo_service import create_user_photo, list_user_photos


router = APIRouter(prefix="/photos", tags=["photos"]) 


@router.post("/", response_model=UserPhotoRead)
def upload_photo(payload: UserPhotoCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # In a real system, you would accept multipart upload; here we accept an image_url
    photo = create_user_photo(db, user_id=current_user.user_id, image_url=payload.image_url)
    return photo


@router.get("/", response_model=list[UserPhotoRead])
def list_photos(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_user_photos(db, user_id=current_user.user_id)

