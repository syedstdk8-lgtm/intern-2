
from enum import Enum
from typing import List, Optional
from fastapi import FastAPI, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Enum as SQLEnum, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, relationship

app = FastAPI()
Base = declarative_base()

class MuscleGroup(str, Enum):
    CHEST = "chest"
    BACK = "back"
    LEGS = "legs"
    SHOULDERS = "shoulders"
    ARMS = "arms"
    CORE = "core"

class Exercise(Base):
    __tablename__ = "exercises"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    muscle_group = Column(SQLEnum(MuscleGroup), nullable=False)
    equipment = Column(String(50), default="bodyweight")

class WorkoutPlan(Base):
    __tablename__ = "workout_plans"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    items = relationship("PlanItem", cascade="all, delete-orphan")

class PlanItem(Base):
    __tablename__ = "plan_items"
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("workout_plans.id"))
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    target_sets = Column(Integer, default=3)
    target_reps = Column(Integer, default=10)

class ExerciseSchema(BaseModel):
    name: str
    muscle_group: MuscleGroup
    equipment: Optional[str] = "bodyweight"

class ExerciseOut(ExerciseSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)

app = FastAPI(title="Exercise Management API", version="1.0.0")

@app.get("/exercises", response_model=List[ExerciseOut])
def get_exercises():
    return []

@app.post("/exercises", response_model=ExerciseOut, status_code=status.HTTP_201_CREATED)
def add_exercise(exercise: ExerciseSchema):
    return {**exercise.model_dump(), "id": 1}