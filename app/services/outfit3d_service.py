import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.models import Outfit, Outfit3D


ALLOWED_3D_FORMATS = {"glb", "gltf", "fbx"}


def get_static_root() -> Path:
    root = Path("static/3d")
    root.mkdir(parents=True, exist_ok=True)
    return root


def store_3d_file(file: UploadFile, outfit_id: int) -> str:
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_3D_FORMATS:
        raise ValueError("Unsupported 3D format")

    root = get_static_root()
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    safe_name = f"outfit_{outfit_id}_{ts}.{ext}"
    dest_path = root / safe_name

    with dest_path.open("wb") as out:
        out.write(file.file.read())

    base_url = settings.media_base_url.rstrip("/") if settings.media_base_url else ""
    if base_url:
        return f"{base_url}/3d/{safe_name}"
    return f"/static/3d/{safe_name}"


def upsert_outfit3d(db: Session, outfit: Outfit, file_url: str, fmt: str) -> Outfit3D:
    existing: Optional[Outfit3D] = db.query(Outfit3D).filter(Outfit3D.outfit_id == outfit.outfit_id).first()
    if existing:
        existing.file_url = file_url
        existing.format = fmt
        db.add(existing)
        db.commit()
        db.refresh(existing)
        return existing
    record = Outfit3D(outfit_id=outfit.outfit_id, file_url=file_url, format=fmt)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_outfit3d(db: Session, outfit_id: int) -> Optional[Outfit3D]:
    return db.query(Outfit3D).filter(Outfit3D.outfit_id == outfit_id).first()

