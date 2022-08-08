import typing as t

from sqlalchemy.orm import Session

from ..schemas import QuestStagesCreateSchema
from ..models.quest_stages import QuestStages


def create_quest_stage(
        db: Session, quest_stage: QuestStagesCreateSchema, quest_id: int
):
    db_quest_stage = QuestStages(**quest_stage.dict(), quest_id=quest_id)
    db.add(db_quest_stage)
    db.commit()
    db.refresh(db_quest_stage)
    return db_quest_stage


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
