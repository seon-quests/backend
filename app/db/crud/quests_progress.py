import datetime
import typing as t
from datetime import timedelta

from sqlalchemy.orm import Session

from app.db.models.quests_progress import QuestsProgress
from app.db.schemas.quests_progress import QuestProgressCreateSchema
from app.db.crud import get_quest


def get_progresses_for_team(
        db: Session, quest_id: int, team_id: int
) -> t.List[QuestsProgress]:
    return db.query(QuestsProgress).filter(
            QuestsProgress.quest_id == quest_id,
            QuestsProgress.team_id == team_id
    ).order_by(QuestsProgress.current_stage_index.asc()).all()


def get_last_quest_progress_for_team(
        db: Session, quest_id: int, team_id: int
) -> t.Optional[QuestsProgress]:
    quest_team_progresses = get_progresses_for_team(
        db=db, quest_id=quest_id, team_id=team_id
    )
    if len(quest_team_progresses) > 0:
        return quest_team_progresses[-1]
    return


def calculate_time_to_answer_stage(
        db: Session, quest_id: int,
        quest_team_last_progress: t.Optional[QuestsProgress]
) -> timedelta:
    if quest_team_last_progress:
        start_time = quest_team_last_progress.answered_at
    else:
        quest = get_quest(db=db, quest_id=quest_id)
        start_time = quest.start_datetime
    return datetime.datetime.now() - start_time


def create_quest_progress(
        db: Session, quest_progress: QuestProgressCreateSchema
) -> QuestsProgress:
    db_quest_progress = QuestsProgress(
        **quest_progress.dict()
    )
    db.add(db_quest_progress)
    db.commit()
    db.refresh(db_quest_progress)
    return db_quest_progress
