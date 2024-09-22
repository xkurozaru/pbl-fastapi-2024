from sqlalchemy.orm import Session

from app.model.users import User


def read_users(db: Session):
    users = db.query(User).order_by(User.id).all()
    return users


def create_user(db: Session, user: User):
    db.add(user)
    db.commit()


def destroy_user(db: Session, id: str):
    db.query(User).filter(User.id == id).delete()
    db.commit()
