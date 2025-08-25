from typing import Optional

from sqlalchemy.orm import Session

from app.models.models import Outfit


def create_outfit(db: Session, name: str, category: str, image_url: str, metadata: dict) -> Outfit:
    outfit = Outfit(name=name, category=category, image_url=image_url, meta=metadata or {})
    db.add(outfit)
    db.commit()
    db.refresh(outfit)
    return outfit


def get_outfit(db: Session, outfit_id: int) -> Optional[Outfit]:
    return db.get(Outfit, outfit_id)


def list_outfits(db: Session, skip: int = 0, limit: int = 50) -> list[Outfit]:
    return db.query(Outfit).order_by(Outfit.created_at.desc()).offset(skip).limit(limit).all()


def update_outfit(db: Session, outfit: Outfit, updates: dict) -> Outfit:
    for key, value in updates.items():
        if value is not None:
            if key == "metadata":
                setattr(outfit, "meta", value)
            else:
                setattr(outfit, key, value)
    db.add(outfit)
    db.commit()
    db.refresh(outfit)
    return outfit


def delete_outfit(db: Session, outfit: Outfit) -> None:
    db.delete(outfit)
    db.commit()

