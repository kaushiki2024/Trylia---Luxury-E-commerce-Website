from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.models.models import User


def create_user(db: Session, name: str, email: str, password: str) -> User:
    user = User(name=name, email=email, password_hash=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> str | None:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    token = create_access_token(user.user_id)
    return token

