from datetime import datetime
import typing as t

from pydantic import BaseModel
from ..models.quests import QuestStatuses
from .teams import TeamResults
from .quest_registered_teams import QuestRegisteredTeamsOutSchema


class QuestBase(BaseModel):
    name: str
    description: str = None
    start_datetime: datetime
    has_plug_stage: bool


class QuestOut(QuestBase):
    id: int
    status: QuestStatuses

    class Config:
        orm_mode = True


class QuestCreate(QuestBase):

    class Config:
        orm_mode = True


class QuestEdit(QuestBase):
    name: t.Optional[str]
    status: t.Optional[QuestStatuses]
    start_datetime: t.Optional[datetime]
    has_plug_stage: t.Optional[bool]

    class Config:
        orm_mode = True


class QuestResults(BaseModel):
    start_datetime: datetime
    total_stages: int = 0
    teams_with_progresses: t.List[TeamResults]

    class Config:
        orm_mode = True


class QuestTeams(BaseModel):
    teams: t.List[QuestRegisteredTeamsOutSchema]

    class Config:
        orm_mode = True
