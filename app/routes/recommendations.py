from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.models import User
from app.schemas.schemas import RecommendationCreate, RecommendationRead
from app.services.recommendation_service import create_recommendation, list_recommendations_for_user


router = APIRouter(prefix="/recommendations", tags=["recommendations"]) 


@router.post("/", response_model=RecommendationRead)
def create_rec(payload: RecommendationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rec = create_recommendation(db, user_id=current_user.user_id, outfit_id=payload.outfit_id, score=payload.score)
    return rec


@router.get("/", response_model=list[RecommendationRead])
def list_recs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_recommendations_for_user(db, user_id=current_user.user_id)

