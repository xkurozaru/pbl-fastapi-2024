from sqlalchemy.orm import Session

from app.model.items import Item


def read_items(db: Session, user_id: str):
    users = db.query(Item).filter(Item.user_id == user_id).order_by(Item.id).all()
    return users


def create_item(db: Session, item: Item):
    db.add(item)
    db.commit()


def destroy_item(db: Session, user_id: str, id: str):
    db.query(Item).filter(Item.user_id == user_id, Item.id == id).delete()
    db.commit()
