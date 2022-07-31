from sqlalchemy import UniqueConstraint, Column, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.db.session import Base


class QuestRegisteredTeams(Base):
    __tablename__ = "quest_registered_teams"
    __table_args__ = (
        UniqueConstraint(
            'team_id', 'quest_id',
        ),
        {'extend_existing': True}
    )

    team_id = Column(ForeignKey('team.id'), primary_key=True)
    quest_id = Column(ForeignKey('quest.id'), primary_key=True)
    is_accepted = Column(Boolean, nullable=True, default=None)
    is_started = Column(Boolean, nullable=False, default=False)
    is_finished = Column(Boolean, nullable=False, default=False)

    team = relationship("Team", back_populates="quests")
    quest = relationship("app.db.models.quests.Quest", back_populates="teams")
