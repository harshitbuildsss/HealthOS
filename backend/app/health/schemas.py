from datetime import date, datetime

from pydantic import BaseModel, Field


class WaterCreate(BaseModel):
    amount_ml: int = Field(gt=0, le=10000)


class WaterResponse(BaseModel):
    id: int
    amount_ml: int
    logged_at: datetime


class SleepCreate(BaseModel):
    sleep_date: date
    duration_minutes: int = Field(gt=0, le=1440)
    quality: int | None = Field(default=None, ge=1, le=5)


class SleepResponse(BaseModel):
    id: int
    sleep_date: date
    duration_minutes: int
    quality: int | None


class ActivityCreate(BaseModel):
    steps: int = Field(ge=0, le=200000)
    exercise_minutes: int = Field(default=0, ge=0, le=1440)


class ActivityResponse(BaseModel):
    id: int
    steps: int
    exercise_minutes: int
    logged_at: datetime


class WeightCreate(BaseModel):
    weight_kg: float = Field(gt=0, le=500)


class WeightResponse(BaseModel):
    id: int
    weight_kg: float
    recorded_at: datetime
