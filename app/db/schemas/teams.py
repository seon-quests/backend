import typing as t
from pydantic import BaseModel

from app.db.schemas.users import UserShortInfoOut
from .quests_progress import QuestProgressOutSchema


class TeamBase(BaseModel):
    name: str


class TeamOut(TeamBase):
    id: int
    quests: "t.Optional[t.List[QuestRegisteredListOutForTeam]]" = []

    class Config:
        orm_mode = True


class TeamWithCaptainOut(TeamBase):
    captain: UserShortInfoOut

    class Config:
        orm_mode = True


class TeamCreate(TeamBase):

    class Config:
        orm_mode = True


class TeamEdit(TeamBase):
    name: str

    class Config:
        orm_mode = True


class TeamResults(TeamBase):
    progresses: t.List[QuestProgressOutSchema]

    class Config:
        orm_mode = True


from .quest_registered_teams import QuestRegisteredListOutForTeam
TeamOut.update_forward_refs()
