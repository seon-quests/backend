from fastapi import APIRouter, Request, Depends, Body
from starlette.responses import JSONResponse

from app.db.session import get_db
from app.db.crud import (
    get_quest,
    create_register_team_for_quest,
    get_registered_team_for_quest
)
from app.db.schemas import QuestRegisteredTeamsCreateSchema
from app.core.auth import get_current_active_user, get_current_active_superuser
from app.db.models import QuestRegisteredTeams
from app.db.crud import get_team_for_player

quest_registered_teams_router = r = APIRouter(
    prefix="/quests/{quest_id}"
)


@r.post("/team-for-quest", response_description='Aga, done')
async def register_team_for_quest(
    request: Request,
    quest_registered_team: QuestRegisteredTeamsCreateSchema,
    quest_id: int,
    db=Depends(get_db)
) -> QuestRegisteredTeams:
    """
    Register team to a quest
    """
    get_quest(db, quest_id=quest_id)
    return create_register_team_for_quest(db, quest_id, quest_registered_team)


@r.post("/started", response_description='Marking quests as started')
async def mark_quest_as_started(
    request: Request,
    quest_id: int,
    db=Depends(get_db),
    user=Depends(get_current_active_user),
) -> JSONResponse:
    """
    Register team to a quest
    """
    team = get_team_for_player(db=db, user_id=user.id)
    registered_team_for_quest = get_registered_team_for_quest(
        db=db, quest_id=quest_id, team_id=team.id
    )
    registered_team_for_quest.is_started = True
    db.commit()
    return JSONResponse(
        status_code=200,
        content={"detail": "quest marked as started"}
    )


@r.post(
    "/team-acceptance",
    response_description='Accepting or declining team for a quest'
)
async def change_registered_team_acceptance_status(
    request: Request,
    quest_id: int,
    team_id: int = Body(..., embed=True),
    acceptance_status: bool = Body(..., embed=True),
    db=Depends(get_db),
    user=Depends(get_current_active_superuser),
) -> JSONResponse:
    """
    Change registered team acceptance status
    """
    registered_team_for_quest = get_registered_team_for_quest(
        db=db, quest_id=quest_id, team_id=team_id
    )
    registered_team_for_quest.is_accepted = acceptance_status
    db.commit()
    return JSONResponse(
        status_code=200,
        content={"detail": f"team acceptance: {acceptance_status}"}
    )
