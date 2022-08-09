from sqlalchemy import (
    Column, ForeignKey, Interval, String,
    SmallInteger, Integer, DateTime
)
from sqlalchemy.orm import relationship

from app.db.session import Base


class QuestsProgress(Base):
    __tablename__ = "quests_progress"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(ForeignKey('team.id'), nullable=False)
    quest_id = Column(ForeignKey('quest.id'), nullable=False)
    answer = Column(String, nullable=True)
    time_to_answer = Column(Interval, nullable=False)
    answered_at = Column(DateTime(timezone=True), nullable=False)
    current_stage_index = Column(SmallInteger, nullable=False)

    quest = relationship("Quest", back_populates="teams_progresses")
