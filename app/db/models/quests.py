import enum

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

from app.db.session import Base


class QuestStatuses(enum.Enum):
    __doc__ = '[draft, announced, registration, started, finished]'
    draft = "draft"
    announced = "announced"  # not used for now
    registration = "registration"
    started = "started"
    finished = "finished"


class Quest(Base):
    __tablename__ = "quest"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    start_datetime = Column(DateTime(timezone=True))
    status = Column(ENUM(QuestStatuses))

    stages = relationship("QuestStages", back_populates="quest")
    teams = relationship(
        "QuestRegisteredTeams", back_populates="quest"
    )
    teams_progresses = relationship(
        "QuestsProgress", back_populates="quest"
    )
