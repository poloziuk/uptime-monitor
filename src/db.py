from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base, CheckResult
from src.config import DB_URL

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def save_result(result: dict):
    with SessionLocal() as session:
        db_entry = CheckResult(
            url=result["url"], status=result["status"], response_time=result["time"]
        )
        session.add(db_entry)
        session.commit()


def _row_to_dict(r: CheckResult) -> dict:
    return {
        "id": r.id,
        "url": r.url,
        "status": r.status,
        "response_time": r.response_time,
        "timestamp": r.timestamp,
    }


def get_last_results(limit: int = 10):
    with SessionLocal() as session:
        rows = (
            session.query(CheckResult)
            .order_by(CheckResult.timestamp.desc())
            .limit(limit)
            .all()
        )
        return [_row_to_dict(r) for r in rows]
