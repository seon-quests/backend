import typing as t
from datetime import datetime

from pydantic import BaseModel

from .quests import QuestOut


class QuestStagesBaseSchema(BaseModel):
    order_number: int
    description: str


class QuestStagesOutSchema(QuestStagesBaseSchema):
    id: int
    answer: str

    class Config:
        orm_mode = True


class QuestStagesOutPlayerSchema(QuestStagesBaseSchema):
    id: int

    class Config:
        orm_mode = True


class QuestStagesCreateSchema(QuestStagesBaseSchema):
    answer: str

    class Config:
        orm_mode = True


class QuestStagesEditSchema(QuestStagesBaseSchema):
    order_number: t.Optional[int]
    description: t.Optional[str]
    answer: t.Optional[str]

    class Config:
        orm_mode = True


class QuestCurrentStageSchema(BaseModel):
    quest: QuestOut
    current_stage: QuestStagesOutPlayerSchema
    total_stages: int
    latest_stage: int
    latest_stage_answered_at: datetime = None

    class Config:
        orm_mode = True
