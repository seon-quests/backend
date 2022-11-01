import datetime

import pytest

from app.db.models.quests import Quest, QuestStatuses


@pytest.fixture
def test_quest(test_db) -> Quest:
    """
        Make a test quest in the database
    """
    quest = Quest(
        name="test",
        description='Some cool quests',
        status=QuestStatuses.draft,
        start_datetime=datetime.datetime(2022, 10, 31),
        has_plug_stage=False
    )
    test_db.add(quest)
    test_db.commit()
    return quest


def test_create_quest(client, test_db, superuser_token_headers):
    assert test_db.query(Quest).count() == 0
    response = client.post(
        "/api/v1/quests",
        json={
            "name": "quest",
            "description": "just test quest",
            "start_datetime": "2022-11-01T17:19:34.559Z",
            "has_plug_stage": False
        },
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert test_db.query(Quest).count() == 1


def test_edit_quest(client, test_db, test_quest, superuser_token_headers):
    updated_data = {
        "name": "quest",
        "description": "updated",
        "has_plug_stage": True,
        "start_datetime": "2022-11-01T17:19:34.559Z",
        "status": "registration"
    }
    response = client.patch(
        f"/api/v1/quests/{test_quest.id}",
        json=updated_data,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    updated_data["id"] = test_quest.id
    updated_data.pop("start_datetime")
    response_data = response.json()
    response_data.pop("start_datetime")
    assert response_data == updated_data


def test_fetch_quest(client, test_db, test_quest, superuser_token_headers):
    response = client.get(
        f"/api/v1/quests/{test_quest.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": test_quest.id,
        "name": test_quest.name,
        "description": test_quest.description,
        "has_plug_stage": test_quest.has_plug_stage,
        'start_datetime': test_quest.start_datetime.isoformat(),
        'status': 'draft'
    }
