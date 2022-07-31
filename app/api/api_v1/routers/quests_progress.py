import typing as t
from fastapi import APIRouter, Request, Depends, Response

from app.db.session import get_db
from app.db.crud import get_quest, create_quest_stage, get_quest_stages_list
from app.db.schemas import QuestStagesCreateSchema, QuestStagesOutSchema
from app.core.auth import get_current_active_superuser, get_current_active_user

quest_stages_router = r = APIRouter(
    prefix="/quests/{quest_id}"
)

