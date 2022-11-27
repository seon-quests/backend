import typing as t

from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session, contains_eager

from ..schemas import QuestCreate, QuestEdit, QuestOut
from ..models.quests import QuestStatuses
from app.core.config import AVAILABLE_QUESTS_FOR_PLAYER
from app.db.models import Team, QuestsProgress, Quest, QuestRegisteredTeams


def create_quest(db: Session, quest: QuestCreate):
    db_quest = Quest(**quest.dict(), status=QuestStatuses.draft)
    db.add(db_quest)
    db.commit()
    db.refresh(db_quest)
    return db_quest


def get_quest_by_name(db: Session, name: str, exclude_quest_id: int = None):
    return db.query(Quest).filter(
        Quest.name == name, Quest.id != exclude_quest_id
    ).first()


def get_quest(db: Session, quest_id: int):
    quest = db.query(Quest).filter(Quest.id == quest_id).first()
    if not quest:
        raise HTTPException(status_code=404, detail="Квест не знайдено")
    return quest


def get_quest_with_results(db: Session, quest_id: int):
    # later add to sorting QuestsProgress.current_stage_index
    teams_with_progresses = db.query(Team).filter(
        QuestRegisteredTeams.quest_id == quest_id,
        QuestRegisteredTeams.team_id == Team.id
    ).outerjoin(
        QuestsProgress,
        and_(
            QuestsProgress.team_id == Team.id,
            QuestsProgress.quest_id == quest_id
        )
    ).order_by(Team.id.asc(), QuestsProgress.id.asc()).options(
        contains_eager('progresses')
    ).all()
    quest = db.query(Quest).filter(Quest.id == quest_id).first()
    quest.teams_with_progresses = teams_with_progresses
    return quest


def get_quests(
        db: Session, skip: int = 0, limit: int = 100
) -> t.List[QuestOut]:
    return db.query(Quest).offset(skip).limit(limit).all()


def get_quests_available_for_players(
        db: Session, skip: int = 0, limit: int = 100
) -> t.List[QuestOut]:
    return db.query(Quest).filter(
        Quest.status.in_(AVAILABLE_QUESTS_FOR_PLAYER)
    ).offset(skip).limit(limit).all()


def edit_quest(
        db: Session, quest_id: int, quest: QuestEdit
) -> QuestOut:
    db_quest = get_quest(db, quest_id)
    update_data = quest.dict(exclude_unset=True)
    if "name" in update_data:
        existing_quest = get_quest_by_name(db, quest.name, quest_id)
        if existing_quest:
            raise HTTPException(status_code=400, detail="Квест вже існує")
    for key, value in update_data.items():
        setattr(db_quest, key, value)
    db.add(db_quest)
    db.commit()
    db.refresh(db_quest)
    return db_quest
