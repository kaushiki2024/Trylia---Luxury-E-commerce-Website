from sqlalchemy.orm import Session

from app.models.models import Recommendation


def create_recommendation(db: Session, user_id: int, outfit_id: int, score: int) -> Recommendation:
    recommendation = Recommendation(user_id=user_id, outfit_id=outfit_id, score=score)
    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)
    return recommendation


def list_recommendations_for_user(db: Session, user_id: int) -> list[Recommendation]:
    return (
        db.query(Recommendation)
        .filter(Recommendation.user_id == user_id)
        .order_by(Recommendation.created_at.desc())
        .all()
    )

