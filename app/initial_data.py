#!/usr/bin/env python3

from db.crud import create_user
from db.schemas import UserCreate
from db.session import SessionLocal


def init() -> None:
    db = SessionLocal()

    create_user(
        db,
        UserCreate(
            email="admin@seon-quests.com",
            password="seonadmin123",
            is_active=True,
            is_superuser=True,
        ),
    )


if __name__ == "__main__":
    print("Creating superuser admin@seon-quests.com")
    init()
    print("Superuser created")
