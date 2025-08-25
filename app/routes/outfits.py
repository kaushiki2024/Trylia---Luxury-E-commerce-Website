from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.models import User
from app.schemas.schemas import Outfit3DRead, OutfitCreate, OutfitRead, OutfitUpdate
from app.services.outfit_service import create_outfit, delete_outfit, get_outfit, list_outfits, update_outfit
from app.services.outfit3d_service import get_outfit3d, store_3d_file, upsert_outfit3d


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


@router.post("/{outfit_id}/upload-3d", response_model=Outfit3DRead)
def upload_3d_model(outfit_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    outfit = get_outfit(db, outfit_id)
    if not outfit:
        raise HTTPException(status_code=404, detail="Outfit not found")
    ext = file.filename.split(".")[-1].lower()
    try:
        file_url = store_3d_file(file, outfit_id=outfit_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    model = upsert_outfit3d(db, outfit=outfit, file_url=file_url, fmt=ext)
    return model


@router.get("/{outfit_id}/3d-model", response_model=Outfit3DRead)
def get_3d_model(outfit_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    outfit = get_outfit(db, outfit_id)
    if not outfit:
        raise HTTPException(status_code=404, detail="Outfit not found")
    model = get_outfit3d(db, outfit_id)
    if not model:
        raise HTTPException(status_code=404, detail="3D model not found")
    return model

