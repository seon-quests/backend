import typing as t

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from ..schemas import QuestStagesCreateSchema, QuestStagesEditSchema
from ..models.quest_stages import QuestStages
from ..models.quests import Quest


def create_quest_stage(
        db: Session, quest_stage: QuestStagesCreateSchema, quest_id: int
):
    db_quest_stage = QuestStages(**quest_stage.dict(), quest_id=quest_id)
    db.add(db_quest_stage)
    db.commit()
    db.refresh(db_quest_stage)
    return db_quest_stage


def delete_quest_stage(db: Session, quest_stage_id: int):
    quest_stage = get_quest_stage(db=db, quest_stage_id=quest_stage_id)
    db.delete(quest_stage)
    db.commit()
    return quest_stage


def get_quest_stage(db: Session, quest_stage_id: int) -> QuestStages:
    quest_stage = db.query(QuestStages).filter(
        QuestStages.id == quest_stage_id
    ).first()
    if not quest_stage:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="No such quest stage"
        )
    return quest_stage


def edit_quest_stage(
    db: Session, quest_stage_id: int, quest_stage: QuestStagesEditSchema
) -> QuestStages:
    db_quest_stage = get_quest_stage(db, quest_stage_id)
    update_data = quest_stage.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_quest_stage, key, value)
    db.add(db_quest_stage)
    db.commit()
    db.refresh(db_quest_stage)
    return db_quest_stage


def get_quest_stage_progress_index(
        db: Session,
        quest_stage_id: int, quest: Quest
):
    quest_stage: QuestStages = get_quest_stage(
        db=db, quest_stage_id=quest_stage_id
    )
    all_stages = get_quest_stages_list(db=db, quest_id=quest.id)
    return all_stages.index(quest_stage)


def get_quest_stages_list(
        db: Session, quest_id: int, skip: int = 0, limit: int = 100
) -> t.List[QuestStages]:
    return db.query(QuestStages).filter(
        QuestStages.quest_id == quest_id
    ).order_by(QuestStages.order_number.asc()).offset(skip).limit(limit).all()


def check_answer(db: Session, quest_stage_id: int, answer: str) -> bool:
    original_answer = db.query(QuestStages).filter(
        QuestStages.id == quest_stage_id
    ).first().answer
    original_answer_fmt = ''.join(
        e for e in original_answer if e.isalnum()
    ).lower()
    answer_fmt = ''.join(e for e in answer if e.isalnum()).lower()
    if answer_fmt == original_answer_fmt:
        return True
    return False
