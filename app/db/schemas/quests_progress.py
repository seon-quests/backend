from datetime import timedelta, datetime

from pydantic import BaseModel


class QuestProgressBaseSchema(BaseModel):
    time_to_answer: timedelta
    current_stage_index: int
    answered_at: datetime


class QuestProgressCreateSchema(QuestProgressBaseSchema):
    team_id: int
    quest_id: int
    answer: str

    class Config:
        orm_mode = True


class QuestProgressOutSchema(QuestProgressBaseSchema):

    class Config:
        orm_mode = True
