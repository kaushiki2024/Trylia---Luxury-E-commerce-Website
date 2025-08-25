from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.models import User
from app.schemas.schemas import OutfitCreate, OutfitRead, OutfitUpdate
from app.services.outfit_service import create_outfit, delete_outfit, get_outfit, list_outfits, update_outfit


router = APIRouter(prefix="/outfits", tags=["outfits"]) 


@router.post("/", response_model=OutfitRead, status_code=status.HTTP_201_CREATED)
def create(payload: OutfitCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    outfit = create_outfit(db, name=payload.name, category=payload.category, image_url=payload.image_url, metadata=payload.metadata)
    return outfit


@router.get("/", response_model=list[OutfitRead])
def list_all(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_outfits(db)


@router.get("/{outfit_id}", response_model=OutfitRead)
def get_one(outfit_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    outfit = get_outfit(db, outfit_id)
    if not outfit:
        raise HTTPException(status_code=404, detail="Outfit not found")
    return outfit


@router.patch("/{outfit_id}", response_model=OutfitRead)
def update(outfit_id: int, payload: OutfitUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    outfit = get_outfit(db, outfit_id)
    if not outfit:
        raise HTTPException(status_code=404, detail="Outfit not found")
    updated = update_outfit(db, outfit, updates=payload.dict(exclude_unset=True))
    return updated


@router.delete("/{outfit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(outfit_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    outfit = get_outfit(db, outfit_id)
    if not outfit:
        raise HTTPException(status_code=404, detail="Outfit not found")
    delete_outfit(db, outfit)
    return None

