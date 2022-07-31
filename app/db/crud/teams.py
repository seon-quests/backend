from sqlalchemy.orm import Session

from ..schemas import TeamCreate
from ..models.teams import Team


def create_team(db: Session, team: TeamCreate, user_id: int):
    db_team = Team(**team.dict(), user_id=user_id)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


def get_team_by_name(db: Session, name: str):
    return db.query(Team).filter(Team.name == name).first()


def get_team_for_player(db: Session, user_id: int):
    return db.query(Team).filter(Team.user_id == user_id).first()
