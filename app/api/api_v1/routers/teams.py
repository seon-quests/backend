from fastapi import APIRouter, Request, Depends, HTTPException

from app.db.session import get_db
from app.db.crud import create_team, get_team_by_name, get_team_for_player
from app.db.schemas import TeamOut, TeamCreate
from app.core.auth import get_current_active_user

team_router = r = APIRouter()


@r.post("/teams", response_model=TeamOut)
async def team_create(
    request: Request,
    team: TeamCreate,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    """
    Create a new team
    """
    any_team = get_team_for_player(db, current_user.id)
    if any_team:
        raise HTTPException(status_code=400, detail="У вас вже є команда")
    db_team = get_team_by_name(db, team.name)
    if db_team:
        raise HTTPException(status_code=400, detail="Така команда вже існує")
    return create_team(db, team, current_user.id)


@r.get("/teams/my-team", response_model=TeamOut)
async def team_for_player(
    request: Request,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    """
    Get a team for current player. Made it as a FK, but first one is taken
    """
    return get_team_for_player(db, current_user.id)
