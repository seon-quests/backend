from sqlalchemy.orm import Session

from app.db.schemas import QuestRegisteredTeamsCreateSchema
from app.db.models.quest_registered_teams import QuestRegisteredTeams


def create_register_team_for_quest(
        db: Session,
        quest_id: int,
        quest_registered_team: QuestRegisteredTeamsCreateSchema
):
    db_quest_registered_team = QuestRegisteredTeams(
        **quest_registered_team.dict(), quest_id=quest_id
    )
    db.add(db_quest_registered_team)
    db.commit()
    db.refresh(db_quest_registered_team)
    return db_quest_registered_team


def get_registered_team_for_quest(
        db: Session, quest_id: int, team_id: int
) -> QuestRegisteredTeams:
    return db.query(QuestRegisteredTeams).filter(
        QuestRegisteredTeams.quest_id == quest_id,
        QuestRegisteredTeams.team_id == team_id
    ).first()
