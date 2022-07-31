import os

PROJECT_NAME = "seon-quests"

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
# SQLALCHEMY_DATABASE_URI = 'postgresql://a-orlov:@localhost:5432/seon'

API_V1_STR = "/api/v1"
AVAILABLE_QUESTS_FOR_PLAYER = ["registration", "started"]
