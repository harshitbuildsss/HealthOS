from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.connection import get_db
from app.health.schemas import (
    ActivityCreate,
    ActivityResponse,
    SleepCreate,
    SleepResponse,
    WaterCreate,
    WaterResponse,
    WeightCreate,
    WeightResponse,
)
from app.health.service import (
    create_activity_log,
    create_sleep_log,
    create_water_log,
    create_weight_log,
    get_activity_logs,
    get_sleep_logs,
    get_water_logs,
    get_weight_logs,
)


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.post(
    "/water",
    response_model=WaterResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_water(
    data: WaterCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return create_water_log(db, user_id, data)


@router.get(
    "/water",
    response_model=list[WaterResponse],
)
def list_water(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return get_water_logs(db, user_id)


@router.post(
    "/sleep",
    response_model=SleepResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_sleep(
    data: SleepCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return create_sleep_log(db, user_id, data)


@router.get(
    "/sleep",
    response_model=list[SleepResponse],
)
def list_sleep(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return get_sleep_logs(db, user_id)


@router.post(
    "/activity",
    response_model=ActivityResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_activity(
    data: ActivityCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return create_activity_log(db, user_id, data)


@router.get(
    "/activity",
    response_model=list[ActivityResponse],
)
def list_activity(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return get_activity_logs(db, user_id)


@router.post(
    "/weight",
    response_model=WeightResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_weight(
    data: WeightCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return create_weight_log(db, user_id, data)


@router.get(
    "/weight",
    response_model=list[WeightResponse],
)
def list_weight(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return get_weight_logs(db, user_id)
