import enum

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

from app.db.session import Base


class UserTypes(enum.Enum):
    __doc__ = '[admin, player]'
    admin = "admin"
    player = "player"


class User(Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    type = Column(ENUM(UserTypes))
    # player fields
    instagram = Column(String)
    phone_number = Column(String)
    team = relationship("Team", back_populates="captain")
