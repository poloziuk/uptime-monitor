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
            url=result["url"],
            status=result["status"],
            response_time=result["time"]
        )
        session.add(db_entry)
        session.commit()

def get_last_results(limit=10):
    with SessionLocal() as session:
        return session.query(CheckResult).order_by(CheckResult.timestamp.desc()).limit(limit).all()

def get_results():
    session = SessionLocal()
    results = session.query(CheckResult).all()
    session.close()
    return results