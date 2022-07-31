from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
import uvicorn

from app.api.api_v1.routers.users import users_router
from app.api.api_v1.routers.auth import auth_router
from app.api.api_v1.routers.quests import quests_router
from app.api.api_v1.routers.quest_stages import quest_stages_router
from app.api.api_v1.routers.teams import team_router
from app.api.api_v1.routers.quest_registered_teams import (
    quest_registered_teams_router
)
from app.core import config
from app.db.session import SessionLocal
from app.core.auth import get_current_active_user


app = FastAPI(
    title=config.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api"
)

origins = [
    "http://localhost",
    "http://localhost:3001",
    "https://seon-quests.herokuapp.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response


@app.get("/api/v1")
async def root():
    return {"message": "SEON Quests app is running..."}


# Routers
app.include_router(
    users_router,
    prefix="/api/v1",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(
    quests_router,
    prefix="/api/v1",
    tags=["quests"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(
    quest_stages_router,
    prefix="/api/v1",
    tags=["quest-stages"],
    dependencies=[Depends(get_current_active_user)]
)
app.include_router(
    team_router,
    prefix="/api/v1",
    tags=["teams"],
    dependencies=[Depends(get_current_active_user)]
)
app.include_router(
    quest_registered_teams_router,
    prefix="/api/v1",
    tags=["quest_registered_teams"],
    dependencies=[Depends(get_current_active_user)]
)
app.include_router(auth_router, prefix="/api", tags=["auth"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
