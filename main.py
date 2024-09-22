from fastapi import Body, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import settings, users_database
from app.model import users

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = settings.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World From Fast API!"}


@app.get("/users")
async def get_users(
    db: Session = Depends(get_db),
) -> list[users.UserSchema]:
    us = users_database.read_users(db)
    return [users.UserSchema.model_validate(u) for u in us]


@app.post("/users")
async def post_user(
    name: str = Body(...),
    grade: int = Body(...),
    team: str = Body(...),
    db: Session = Depends(get_db),
) -> users.UserSchema:
    u = users.User(name, grade, team)
    users_database.create_user(db, u)
    return users.UserSchema.model_validate(u)


@app.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
) -> None:
    users_database.destroy_user(db, user_id)
