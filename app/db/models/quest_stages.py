from sqlalchemy import Column, Integer, Text, String, ForeignKey, \
    UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.session import Base


class QuestStages(Base):
    __tablename__ = "quest_stages"
    __table_args__ = (
        UniqueConstraint(
            'order_number', 'quest_id',
        ),
        {'extend_existing': True}
    )

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    answer = Column(String, nullable=False)
    quest_id = Column(Integer, ForeignKey("quest.id"), nullable=False)

    quest = relationship("Quest", back_populates="stages")
