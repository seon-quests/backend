import typing as t
from fastapi import APIRouter, Request, Depends, HTTPException, Response

from app.db.session import get_db
from app.db.crud import (
    create_quest,
    get_quest_by_name,
    get_quest,
    edit_quest,
    get_quests,
    get_quest_with_results,
    get_quests_available_for_players
)
from app.db.schemas import (
    QuestOut, QuestCreate, QuestEdit,
    QuestResults, QuestTeams
)
from app.core.auth import get_current_active_superuser, get_current_active_user

quests_router = r = APIRouter()


@r.get(
    "/quests",
    response_model=t.List[QuestOut],
)
async def quests_list(
    response: Response,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Get all users
    """
    if current_user.is_superuser:
        quests = get_quests(db)
    else:
        quests = get_quests_available_for_players(db)
    return quests


@r.post("/quests", response_model=QuestOut)
async def quest_create(
    request: Request,
    quest: QuestCreate,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """
    Create a new quest
    """
    db_quest = get_quest_by_name(db, quest.name)
    if db_quest:
        raise HTTPException(status_code=400, detail="Квест вже існує")
    return create_quest(db, quest)


@r.get(
    "/quests/{quest_id}",
    response_model=QuestOut,
)
async def quest_details(
    request: Request,
    quest_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """
    Get any quest details
    """
    quest = get_quest(db, quest_id)
    return quest


@r.patch("/quests/{quest_id}", response_model=QuestOut)
async def quest_edit(
    request: Request,
    quest_id: int,
    quest: QuestEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """
    Update existing quest
    """
    return edit_quest(db, quest_id, quest)


@r.get(
    "/quests/{quest_id}/results",
    response_model=QuestResults,
)
async def quest_results(
    request: Request,
    quest_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """
    Get any quest details
    """
    quest = get_quest_with_results(db, quest_id)
    quest.total_stages = len(quest.stages)
    return quest


@r.get(
    "/quests/{quest_id}/teams",
    response_model=QuestTeams,
)
async def quest_teams(
    request: Request,
    quest_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """
    Get all the teams registered for the quest
    """
    quest = get_quest(db, quest_id)
    return quest
