# seon-quests

## Features

- **FastAPI** with Python 3.8

- Postgres
- SqlAlchemy with Alembic for migrations
- Pytest for backend tests

## Development

The only dependencies for this project should be installed from requirements.txt file

### Quick Start

```bash
pip install -r requirements.txt
export DATABASE_URL = your database data
python3 app/main.py
```

And navigate to http://localhost:8000

Auto-generated docs will be at
http://localhost:8000/api/docs


## Migrations

Migrations are run using alembic. To run all migrations:

```
alembic upgrade head
```

To create a new migration:

```
alembic revision -m "create users table"
```

And fill in `upgrade` and `downgrade` methods. For more information see
[Alembic's official documentation](https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script).

### Backend Tests

```
pytest
```

any arguments to pytest can also be passed after this command

## Project Layout

```
backend
└── app
    ├── alembic
    │   └── versions # where migrations are located
    ├── api
    │   └── api_v1
    │       └── routers  # linked functions to the real routes
    │           └── tests  # tests for basic routes, will be extended
    ├── core    # config
    ├── db      # db models
    │   └── crud  # CRUD helper functions
    │   └── models   # SQL Models
    │   └── schemas  # Pydantic schemas
    ├── tests   # only one test that app is running, will be extended
    └── main.py # entrypoint to backend
```
