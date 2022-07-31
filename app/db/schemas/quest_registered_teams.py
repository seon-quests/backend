import typing as t

from pydantic import BaseModel
from app.db.schemas.teams import TeamWithCaptainOut


class QuestRegisteredTeamsBaseSchema(BaseModel):
    is_accepted: t.Optional[bool] = None
    is_started: t.Optional[bool]
    is_finished: t.Optional[bool]


class QuestRegisteredTeamsOutSchema(QuestRegisteredTeamsBaseSchema):
    team: TeamWithCaptainOut
    team_id: int

    class Config:
        orm_mode = True


class QuestRegisteredTeamsCreateSchema(QuestRegisteredTeamsBaseSchema):
    team_id: int

    class Config:
        orm_mode = True


class QuestRegisteredTeamsEditSchema(BaseModel):
    is_accepted: bool
    is_started: bool
    is_finished: bool

    class Config:
        orm_mode = True


class QuestRegisteredListOutForTeam(QuestRegisteredTeamsBaseSchema):
    quest_id: int

    class Config:
        orm_mode = True
