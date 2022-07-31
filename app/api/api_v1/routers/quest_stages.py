import typing as t
from datetime import datetime

from fastapi import APIRouter, Request, Depends, Response, Body
from fastapi.responses import JSONResponse

from app.db.session import get_db
from app.db.crud import (
    get_quest, create_quest_stage, get_quest_stages_list,
    get_team_for_player, get_last_quest_progress_for_team, check_answer,
    create_quest_progress, calculate_time_to_answer_stage
)
from app.db.schemas import (
    QuestStagesCreateSchema, QuestStagesOutSchema,
    QuestCurrentStageSchema, QuestProgressCreateSchema
)
from app.core.auth import get_current_active_superuser, get_current_active_user

quest_stages_router = r = APIRouter(
    prefix="/quests/{quest_id}"
)


@r.post("/quest-stages", response_model=QuestStagesOutSchema)
async def quest_stage_create(
    request: Request,
    quest_stage: QuestStagesCreateSchema,
    quest_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser)
):
    """
    Create a new quest stage
    """
    get_quest(db, quest_id)
    return create_quest_stage(db, quest_stage, quest_id)


@r.get(
    "/quest-stages",
    response_model=t.List[QuestStagesOutSchema],
)
async def quests_list(
    response: Response,
    quest_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """
    Get all users
    """
    quest_stages = get_quest_stages_list(db, quest_id=quest_id)
    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-9/{len(quest_stages)}"
    return quest_stages


@r.get(
    "/current-stage",
    response_model=QuestCurrentStageSchema,
)
async def get_current_stage_details(
    quest_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    """
    Get current stage details
    """
    team = get_team_for_player(db=db, user_id=current_user.id)
    quest_stages = get_quest_stages_list(db, quest_id=quest_id)
    quest_team_last_progress = get_last_quest_progress_for_team(
        db=db, quest_id=quest_id, team_id=team.id
    )
    current_stage_index = 0
    latest_stage_answered_at = None
    if quest_team_last_progress:
        current_stage_index = quest_team_last_progress.current_stage_index + 1
        latest_stage_answered_at = quest_team_last_progress.answered_at
    try:
        current_stage = quest_stages[current_stage_index]
    except IndexError:
        current_stage = quest_stages[current_stage_index-1]
    return QuestCurrentStageSchema(
        current_stage=current_stage,
        quest=current_stage.quest,
        total_stages=len(quest_stages),
        latest_stage=current_stage_index,
        latest_stage_answered_at=latest_stage_answered_at
    )


@r.post(
    "/quest-stages/{quest_stage_id}/answer",
    response_model=t.Optional[QuestCurrentStageSchema],
    status_code=201
)
async def check_quest_stage_answer(
    quest_id: int,
    quest_stage_id: int,
    answer: str = Body(..., embed=True),
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    # working on this one
    if check_answer(db=db, quest_stage_id=quest_stage_id, answer=answer):
        team_id = get_team_for_player(db=db, user_id=current_user.id).id
        quest_team_last_progress = get_last_quest_progress_for_team(
            db=db, quest_id=quest_id, team_id=team_id
        )
        time_to_answer = calculate_time_to_answer_stage(
            db=db, quest_id=quest_id,
            quest_team_last_progress=quest_team_last_progress
        )
        new_index = (
            quest_team_last_progress.current_stage_index + 1
            if quest_team_last_progress
            else 0
        )
        quest_progress = QuestProgressCreateSchema(
            quest_id=quest_id, team_id=team_id, answer=answer,
            time_to_answer=time_to_answer, current_stage_index=new_index,
            answered_at=datetime.now()
        )
        create_quest_progress(db=db, quest_progress=quest_progress)
        current_stage_details = await get_current_stage_details(
            quest_id=quest_id, db=db, current_user=current_user
        )
        return current_stage_details
    return JSONResponse(status_code=202, content={"detail": "oops"})
