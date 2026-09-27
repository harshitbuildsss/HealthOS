from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.dashboard.service import get_dashboard
from app.database.connection import get_db


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("")
def dashboard(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return get_dashboard(db, user_id)