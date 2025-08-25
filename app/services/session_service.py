from sqlalchemy.orm import Session

from app.models.models import TryOnSession


def create_tryon_session(db: Session, user_id: int, photo_id: int | None, outfit_id: int | None, result_url: str | None) -> TryOnSession:
    session = TryOnSession(user_id=user_id, photo_id=photo_id, outfit_id=outfit_id, result_url=result_url)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def list_user_sessions(db: Session, user_id: int) -> list[TryOnSession]:
    return (
        db.query(TryOnSession)
        .filter(TryOnSession.user_id == user_id)
        .order_by(TryOnSession.created_at.desc())
        .all()
    )

