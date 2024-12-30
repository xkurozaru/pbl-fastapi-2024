from sqlalchemy import text
from sqlalchemy.orm import Session


def health_check(
    db: Session,
) -> str:
    result = db.execute(text("SELECT 'Healthy' as message")).fetchone()
    return result[0]
