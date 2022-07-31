
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base


class Team(Base):
    __tablename__ = "team"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    captain = relationship("User", back_populates="team")
    quests = relationship(
        "QuestRegisteredTeams", back_populates="team"
    )
    progresses = relationship("QuestsProgress")
