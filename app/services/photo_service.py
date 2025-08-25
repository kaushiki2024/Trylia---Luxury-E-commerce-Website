from sqlalchemy.orm import Session

from app.models.models import UserPhoto


def create_user_photo(db: Session, user_id: int, image_url: str) -> UserPhoto:
    photo = UserPhoto(user_id=user_id, image_url=image_url)
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo


def list_user_photos(db: Session, user_id: int) -> list[UserPhoto]:
    return db.query(UserPhoto).filter(UserPhoto.user_id == user_id).order_by(UserPhoto.uploaded_at.desc()).all()

