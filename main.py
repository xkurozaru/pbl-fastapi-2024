from fastapi import Body, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import items_database, settings, users_database
from app.model import items, users

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


def get_auth_user_id(authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> str:
    # FIXME: Need to use 〇〇〇
    return authorization.credentials


@app.get("/")
async def root():
    return {"message": "Hello World From Fast API!"}


@app.get("/users")
async def get_users(
    db: Session = Depends(get_db),
) -> list[users.UserSchema]:
    user_list = users_database.read_users(db)
    return [users.UserSchema.model_validate(u) for u in user_list]


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


@app.get("/items")
async def get_items(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_auth_user_id),
) -> list[items.ItemSchema]:
    item_list = items_database.read_items(db, user_id)
    return [items.ItemSchema.model_validate(i) for i in item_list]


@app.post("/items")
async def post_item(
    name: str = Body(...),
    price: int = Body(...),
    db: Session = Depends(get_db),
    user_id: str = Depends(get_auth_user_id),
) -> items.ItemSchema:
    i = items.Item(name, price, user_id)
    items_database.create_item(db, i)
    return items.ItemSchema.model_validate(i)


@app.delete("/items/{item_id}")
async def delete_item(
    item_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_auth_user_id),
) -> None:
    items_database.destroy_item(db, user_id, item_id)
